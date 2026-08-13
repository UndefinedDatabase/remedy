── STEP T003-a / F111 — Round 16 ─────────────────────────────
Goal:
  Record the R15 verdict, resolve R-0316 and R-0317, then make F111 real on
  the PROMPT side: `run_builder_bridge_loop` selects margin-expanded repair
  hunks from the patch it just applied and carries them in the repair context,
  with the chosen mode emitted as evidence. NOTHING has imported the T001/T002
  modules until now; C4 is the commit that ends that.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r16-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md, all three appends in ONE commit, in this order:
      TEXT-A, then TEXT-B, then TEXT-C
  C4  the wiring, in packages/orchestration/builder_bridge.py
  C5  tests, in tests/orchestration/test_builder_repair_loop.py
  C6  replace .agent/plan.md with TEXT-D, then rewrite .agent/handoff.md

Scope — EXACTLY these seven paths, no others:
  1 .agent/authored/f111-r16-1.md   2 .agent/last_block.md
  3 .agent/live_review.md           4 packages/orchestration/builder_bridge.py
  5 tests/orchestration/test_builder_repair_loop.py
  6 .agent/plan.md                  7 .agent/handoff.md

Change — C4, packages/orchestration/builder_bridge.py:
  Add two keyword-only arguments to `run_builder_bridge_loop`, next to the
  existing `max_cycles`: `diff_mode: bool = True` and
  `diff_margin_lines: int = 3` (DECISION F111 D7, recorded in TEXT-C).

  Add ONE module-level private helper directly above `run_builder_bridge_loop`,
  with the one-line WHY comment above the def as this repo's convention
  requires:

    def _attach_diff_repair_hunks(
        repair_ctx: dict[str, Any],
        bridge_result: BridgeResult,
        repo_path: Path,
        *,
        margin_lines: int,
    ) -> dict[str, Any]

  It returns the evidence metadata for the round and mutates `repair_ctx` only
  on the diff path. Order of decisions, each returning immediately:
   - `bridge_result.parse_result` is None, or it has no truthy `patch`
     attribute -> return {"mode": "full_file", "reason": "no_patch"}.
   - `changed_line_ranges_from_patch(patch)` is empty
     -> return {"mode": "full_file", "reason": "no_ranges"}.
   - `select_repair_hunks(repo_path, ranges, margin_lines=margin_lines)`
     returns a selection with no `hunks` -> return
     {"mode": "full_file", "reason": "no_hunks_selected",
      "omitted": [list(entry) for entry in selection.omitted]}.
   - Otherwise set `repair_ctx["diff_hunks"]` to a list of dicts, one per
     hunk, keys `path`, `start_line`, `end_line`, `text`, in the selection's
     own order; set `repair_ctx["diff_hunks_omitted"]` to
     [list(entry) for entry in selection.omitted]; and return
     {"mode": "diff", "hunk_count": <len>, "total_chars": selection.total_chars,
      "omitted": [list(entry) for entry in selection.omitted]}.

  Import `select_repair_hunks` and `changed_line_ranges_from_patch` from
  `packages.orchestration.diff_repair` at the same place the loop already
  imports `build_repair_context` — inside `run_builder_bridge_loop`'s body if
  the helper can reach them, otherwise at module level; do not change any
  existing import.

  In `run_builder_bridge_loop`, inside the existing
  `if bridge_result.test_passed is False and cycle < max_cycles:` branch,
  AFTER `loop_result.repair_contexts.append(repair_ctx)` and BEFORE the
  existing `repair_context_created` emit, insert:

    if diff_mode:
        mode_meta = _attach_diff_repair_hunks(
            repair_ctx, bridge_result, repo_path,
            margin_lines=diff_margin_lines,
        )
    else:
        mode_meta = {"mode": "full_file", "reason": "diff_mode_off"}
    repair_ctx["repair_mode"] = mode_meta["mode"]
    _emit(data_dir, job.id, "repair_mode_selected", {"cycle": cycle, **mode_meta})

  Leave the `repair_context_created` emit exactly as it is. Change nothing
  else in the loop: not the cycle bounds, not the repeated-patch detection,
  not the stop reasons, not `run_builder_bridge`, and nothing in
  `repair_context.py`, `diff_repair.py`, `diff_repair_response.py`,
  `diff_repair_apply.py` or `source_apply.py`.

  Two deliberate absences, each stated as a one-line comment where a reader
  would search for it:
   - The emitted metadata carries COUNTS ONLY — `hunk_count`, `total_chars`,
     `omitted` — and never hunk TEXT. `build_repair_context`'s contract is that
     its dict is safe to log; source text belongs in the prompt, not the
     timeline.
   - `mode` here is `diff` or `full_file`, the PROMPT-side choice.
     `full_fallback` is the APPLY-side outcome that `diff_repair_apply` already
     names and that R17 wires; the two vocabularies stay separate on purpose.

  Before committing C4, run `rg -n 'repair_ctx\[|repair_context' tests/` and
  read every assertion that pins the repair-context dict's KEY SET. If any test
  asserts an exact key set, STOP, do not widen it, and report it in the
  handback — a fixed key set is a contract this block did not budget for.

Change — C5, tests/orchestration/test_builder_repair_loop.py:
  Add THREE tests to the existing file, reusing whatever job/data_dir
  scaffolding the file already uses. Do not modify the six tests already there.

  1. `test_diff_mode_attaches_margin_expanded_hunks_to_the_repair_context`
     Drive the loop so cycle 1 applies a unified-diff patch and its test run
     fails, and cycle 2 is reached. Assert the cycle-1 repair context carries
     `repair_mode == "diff"` and a non-empty `diff_hunks` list whose first entry
     has `path`, `start_line`, `end_line` and a `text` that contains a line the
     margin pulled in and that the patch itself did NOT change — that is what
     proves the MARGIN, not merely the selection.
  2. `test_diff_mode_off_leaves_the_repair_context_on_the_full_file_path`
     Same drive, `diff_mode=False`. Assert `repair_mode == "full_file"`,
     `"diff_hunks" not in repair_ctx`, and that a `repair_mode_selected` event
     exists with `reason == "diff_mode_off"`. This is the feature file's
     "Diff mode off -> behavior byte-identical to today" acceptance line.
  3. `test_a_patch_without_line_ranges_reports_full_file_with_a_reason`
     Drive cycle 1 with a `file_ops`-only patch. Assert `repair_mode ==
     "full_file"` and that the emitted `repair_mode_selected` metadata's
     `reason` is `no_ranges` or `no_hunks_selected` — DECISION F111 D3 says a
     file_ops path maps to an empty range list, and the point of the assertion
     is that the reason is VISIBLE, never silently absent.

  Read the events with the same loader the module uses
  (`packages.orchestration.timeline.load_run_events`), not by re-reading a file
  path by hand.

Constraints:
  - SPLIT round. You are the worker; you make every commit. AGENTS.md is the
    highest authority: self-review loop before every commit, plan.md current,
    clean tree, push after each commit.
  - Never work on main, never force-push, never merge. No PR this round.
  - Destructive checks (the ordered mutation probe) run ONLY inside a
    disposable `git worktree`, which you remove before the handback;
    `git status --porcelain` in the primary checkout is empty at every commit
    and at the handback.
  - Do NOT write a `Done:` paragraph of your own in `.agent/live_review.md`
    (planner_reviewer_prompt.md §4.4). TEXT-A and TEXT-B below are the only
    `Done:` text this round applies. If you land a fix this block did not
    order, mark it `Landed: R-XXXX — <one line>` instead.
  - Apply TEXT-A, TEXT-B, TEXT-C, TEXT-D BYTE FOR BYTE. If a text violates a
    rule, do not repair it — apply it and declare the deviation.
  - If any gate below is red, or the block contradicts the code you find, stop
    at that point, commit what is clean, and say so in the handback. Do not
    widen scope to route around it.

Done when — every command run for real, exit code recorded, no value guessed:
  a. TRANSPORT: `sha256sum .agent/authored/f111-r16-1.md .agent/last_block.md`
     -> both digests identical, and `cmp` of the two exits 0. State the digest,
     the byte count, and `wc -l` of the authored file, which must be under 400.
  b. `.agent/live_review.md`: `grep -c '^Done:'` -> 11 (was 9);
     `grep -c '^- R-0'` -> 42 (unchanged, no finding registered this round);
     `grep -c '^### R15 — PASS'` -> 1; `grep -c '^Landed:'` -> prints 0.
  c. `grep -n '_attach_diff_repair_hunks' packages/orchestration/builder_bridge.py`
     -> exactly 2 hits (the def and the one call site).
     `grep -c 'repair_mode_selected' packages/orchestration/builder_bridge.py`
     -> 1.
  d. VALUE PROBE, diff mode on: print the cycle-1 repair context's
     `repair_mode` and the `path`/`start_line`/`end_line` of its first
     `diff_hunks` entry. Paste the exact printed values.
  e. VALUE PROBE, diff mode off: print `repair_mode` and
     `'diff_hunks' in repair_ctx`. Expected exactly `full_file` and `False`.
  f. `python3 -m pytest tests/orchestration/test_builder_repair_loop.py -q`
     -> 9 passed (was 6).
  g. `python3 -m pytest tests/orchestration/test_diff_repair.py
     tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_diff_repair_apply.py -q` -> 71 passed, unmoved.
  h. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` -> 42 passed.
  i. MUTATION PROBE, in a disposable worktree only: replace the body of
     `_attach_diff_repair_hunks` with `raise AssertionError("mutant")` and
     report WHICH tests fail and how many. Report the real result whatever it
     is — if nothing fails, say so; that would mean the new tests do not reach
     the helper, which is a finding and not your fault. Remove the worktree and
     show `git worktree list`.
  j. `git status --porcelain` -> empty. `git diff --name-only 48c6340e..HEAD`
     restricted to this round's commits -> exactly the seven scoped paths.
     Per-commit insertions from `git log --numstat`, each under 500.
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> 0 and 0 after the final push.

Handback: completion report + rewrite .agent/handoff.md (item-status table for
C1-C6, changed-files table, the ten gate results a-j with their real values,
open-findings count, next expected action). Repeat the Fortschritt line from
TEXT-D verbatim. Do not write your own insertion count for C6 inside C6.

──────────────────────── TEXT-A — append to .agent/live_review.md ───────────

Done: R-0316 — the diff-repair seam no longer reports a clean tree it cannot
guarantee. `apply_diff_repair` reads the applicator's own error strings for
`rollback_incomplete`, carries the flag on `DiffRepairApplyResult`, and passes
`apply_result.files_modified` through instead of a hardcoded 0 when the restore
did not finish. Verified at the R16 gate by mutation, inside a disposable
worktree that was removed before the verdict: reverting that one expression to
`files_modified=0` fails exactly
`test_incomplete_rollback_reports_the_real_count_not_a_clean_tree` with
`assert 0 == 1`, so the test pins the behaviour rather than describing it. The
complete-rollback direction is pinned in the same round by the two assertions
added to `test_conflicting_hunk_falls_back_and_leaves_both_files_untouched`
(`rollback_incomplete is False`, `files_modified == 0`), so "always report a
count" cannot satisfy the pair. Noted, not registered: the count is the
applicator's total for the attempt, not the number of files whose restore
actually failed, so it over-reports rather than under-reports — the safe
direction for a seam whose whole purpose is to stop under-claiming damage.
Resolved.

──────────────────────── TEXT-B — append to .agent/live_review.md ───────────

Done: R-0317 — the blank-context repair no longer eats a file separator.
`_blank_line_is_hunk_body` scans forward from the blank for the first non-blank
entry and returns False at `---`, `+++`, `diff ` or end of input, so the
rewrite branch now needs the lookahead as well as the budget. Verified at the
R16 gate by value and by mutation, both re-run by the reviewer on this machine:
`normalize_diff_blank_context` is byte-identity on the two-file over-declared
shape, `split_diff_by_path` returns both sections, and the first section
applies to 'import os\nvalue = 1\nmore = 3\n' returning
'import os\nvalue = 2\nmore = 3\n' — where before the fix it returned None.
Deleting the `_blank_line_is_hunk_body(lines, index + 1)` conjunct in a
disposable worktree fails exactly the three tests R15 added for it and nothing
else. R-0313 stays closed under the same probe: 'a\n\nB\n'. Resolved.

──────────────────────── TEXT-C — append to .agent/live_review.md ───────────

### R15 — PASS (2026-08-13)
Reviewed by the main session over 48c6340e..d457219a. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport is
the PRIMARY cmp proof, not the digest fallback: the previous session's
scratchpad originals survived in `.remedy-wt/f111r15/`, and
`cmp .remedy-wt/f111r15/BLOCK .agent/authored/f111-r15-1.md`,
`cmp .remedy-wt/f111r15/BLOCK .agent/last_block.md` and
`cmp .remedy-wt/f111r15/PLAN .agent/plan.md` all exit 0. The three live_review
appends each occur exactly once in the file, in the ordered sequence. Markers
counted: nine `Done:` lines, 42 registered findings, one R14 gate heading, zero
unreviewed `Landed:` lines. Scope: exactly the nine ordered paths. Per-commit
insertions 341/266/81/40/49/91/92, each under 500. `git status --porcelain`
empty, one worktree, and 0 ahead and 0 behind the remote.

Tests re-run by the reviewer: 71 for the three diff-repair files (was 68), 55
for the applier tier — unmoved, as the applier was not touched — and 42 for the
golden-path canary. Both value probes reproduce exactly: the normaliser is
byte-identity on the two-file over-declared shape and its first section applies
to 'import os\nvalue = 2\nmore = 3\n', and R-0313 still yields 'a\n\nB\n'.
Mutation red-proofs ran inside a disposable git worktree, which was removed
before this verdict: deleting the `_blank_line_is_hunk_body` conjunct fails
exactly the three R-0317 tests, and reverting `files_modified` to a hardcoded 0
fails exactly the one R-0316 test. Both fixes are pinned, not merely present.

Both of the round's declared notes are upheld. The "Nine proofs" docstring line
was a sentence this round's own edits falsified, and correcting it inside a
file the block already ordered is right. The block did say "EXACTLY these eight
paths" over an enumeration of nine; the enumeration was operative and the
worker read it that way. That is a defect in the R15 block, which the reviewer
wrote, and it is noted here rather than registered because the round lost
nothing to it.

Also noted, not registered: R15 fixed R-0316 and R-0317 without the unreviewed-
fix marker §4.4 describes, because the R15 block itself gated that marker to
zero. The property §4.4 protects is that an unreviewed fix must never read as
resolved; leaving both entries at OPEN under-claims rather than over-claims, so
the property held, and the information the marker carries was in the handoff.
The rule stands unchanged for the next round that lands a fix ahead of its
verdict.

DECISION F111 D7 (2026-08-13, reviewer, authored for R16) — the repair-mode
knobs are keyword arguments on `run_builder_bridge_loop`, not a new config
module. The feature file asks for "Config: repair.diff_mode (default on),
context margin lines". This repository has no `packages/config`, and the loop
already takes its bounds as keyword arguments (`max_cycles`, `autonomy_level`),
so `diff_mode: bool = True` and `diff_margin_lines: int = 3` join them there.
Alternative considered and rejected for v1: a settings record read from disk,
which would add a new contract, a new file format and new tests to a slice
whose whole job is wiring. Reverse this decision by moving the two arguments
into a settings record and deleting this paragraph.

──────────────────── TEXT-D — full replacement of .agent/plan.md ────────────

# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: d457219a (R15 PASS).
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
R16 is T003's prompt half and the round that makes F111 real: until
this commit nothing imported the T001/T002 modules.
`run_builder_bridge_loop` maps the patch it just applied to changed
line ranges, selects margin-expanded hunks, carries them in the
repair context, and emits `repair_mode_selected` with counts only.
`diff_mode` and `diff_margin_lines` are keyword arguments per
DECISION F111 D7. T001 and T002 are complete and repaired.

## Next Steps
1. R17 — T003's apply half: route the builder's diff answer through
   `apply_diff_repair`, emit the apply-side mode and token actuals,
   and add the fixture comparison test that records both modes'
   token counts (the feature's DONE condition).
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- The prompt side now carries hunk TEXT in the repair context. Only
  counts go into the timeline; any later change that logs the whole
  context would leak source into evidence.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.

Fortschritt: ~80 % (T001 ✅ · T002 ✅ · T003 Prompt-Hälfte in dieser Runde ·
T003 Apply-Hälfte offen · R-0316 ✅ · R-0317 ✅) — Schätzung
