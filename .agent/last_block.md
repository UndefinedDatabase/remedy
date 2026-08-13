── STEP R9/4 — F111 Diff-only repair — T002b: the per-path diff split ────────
Goal:        Persist the R8 gate, resolve R-0307 and register R-0308, then
             build the conversion the apply half needs: a per-path split of a
             multi-file unified diff, living INSIDE `review_scope` where the
             repository's single reading of hunk headers already lives, and a
             `DiffRepairResponse` -> `StructuredPatch` conversion built on it.
             The apply-and-fallback half is R10 and is NOT in this round.
Bundle:      C1 block save; C2 last_block mirror; C3 gate+finding append;
             C4 resolve R-0307; C5 review_scope split + tests;
             C6 response-to-patch conversion + tests; C7 plan + handoff.
             Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r9-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md,
             packages/orchestration/review_scope.py,
             packages/orchestration/diff_repair_response.py,
             tests/orchestration/test_review_scope.py,
             tests/orchestration/test_diff_repair_response.py.
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS
             SCRATCH FILE (`cat` / `cp`) — never retype, never reflow.
             Do NOT touch `.agent/candidates.md` or `.agent/decisions.md`.
             Do NOT touch `diff_repair.py`, `source_apply.py`,
             `structured_patch.py`, `builder_bridge.py`, `repair_context.py`
             or `pingpong_loop.py`.
             Write no `Done:` and no `Landed:` line of your own: the ONE
             `Done:` text C4 applies is reviewer-authored and is given to you
             verbatim (docs/agents/planner_reviewer_prompt.md §4.4).

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 456a25e9.
   Any mismatch => STOP and hand back.  `mkdir -p .remedy-wt/f111r9`.

1. C1 — Save this ENTIRE step block (from the `── STEP R9/4` line through the
   final `Handback:` line, byte for byte) to `.remedy-wt/f111r9/BLOCK`, then
   `cp .remedy-wt/f111r9/BLOCK .agent/authored/f111-r9-1.md`; `cmp` silent.
   Commit: chore(f111): save the R9 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r9-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R9 block into last block   -> push

3. C3 — GATE AND FINDING FIRST. Write the slice delimited by `<<<LRG_BEGIN`
   and `<<<LRG_END` (marker lines excluded) to `.remedy-wt/f111r9/LRG`, then
   `cat .remedy-wt/f111r9/LRG >> .agent/live_review.md`.
   PURE APPEND: in `git show --numstat <C3> -- .agent/live_review.md` the
   DELETE column must be exactly `0`; report the real insertion count rather
   than matching a number stated from memory. A nonzero delete column means a
   rewrite: STOP and hand back.
   Commit: chore(f111): record the R8 gate and finding R-0308   -> push

<<<LRG_BEGIN

### R8 — PASS (2026-08-13)
Reviewed by the main session over 023e8d9d..456a25e9. Every ordered gate was
re-run by the reviewer, and the new module was additionally probed live, never
read off the handback. Transport: PRIMARY cmp proof, no digest fallback —
`.remedy-wt/f111r8/BLOCK`, `.agent/authored/f111-r8-1.md` and
`.agent/last_block.md` are byte-identical, `.remedy-wt/f111r8/PLAN` and
`.agent/plan.md` are byte-identical, and a `str.count` of the appended slice
against `.agent/live_review.md` prints 1. Append purity by numstat: `36 0` for
the gate commit and `4 1` for the header pair, the single deletion being the
retired counter line and nothing else. Markers on the final file: 32 `- R-0`,
4 `Done:`, 1 `Landed:`, 1 `### R7 — PASS`. Caps: the plan is 48 lines and
carries `## Goal` and `## Next Steps`; the step block is 356 lines, under the
DECISION F105 D5 limit of 400; per-commit insertions 356/341/36/4/50/439/111,
each under 500. Tests: `python3 -m pytest
tests/orchestration/test_diff_repair_response.py
tests/orchestration/test_diff_repair.py tests/cli/test_golden_path.py -q` exit
0, 95 passed — 23 new, the 30 T001 tests unchanged, 42 canary; `python3 -m
pytest tests/orchestration/test_source_apply.py
tests/orchestration/test_source_apply_transaction.py
tests/orchestration/test_fence_e2e.py tests/test_path_utils.py
tests/test_data_paths.py -q` exit 0, 225 passed — the 174 behaviour pin the
reviewer measured BEFORE the round, unchanged, plus the 51 repo-wide guards
that rglob every `packages/**/*.py` and therefore already reach the new module.
Reviewer's own probe, beyond the ordered gates: a two-file diff declared with
one path returned exactly `diff touches undeclared path: src/b.py`; a ghost
declaration returned exactly `declared path not touched by the diff:
src/ghost.py`; `precheck_diff_repair_fences` denied `remedy.toml` with reason
`denied:builtin:project config file`, and denied a path lying outside a job
allow glob. The C5 reuse is real, not nominal: the three path-safety message
strings moved into `unsafe_path_issues` unchanged and `validate_structured_patch`
now calls it. Hygiene: `git status --porcelain` empty, `git worktree list` one
entry, remote comparison `0 0`. Scope: exactly the eight ordered paths.

Deviation ACCEPTED: C4's `Landed:` line names `commit C4 of R8` instead of its
own short sha. A commit cannot carry its own sha without amending, the block
named that fallback explicitly, and the handoff's item-status table declares
C4 `deviated` with that reason — finding R-0306 repaired on its first occasion
after being registered.

- R-0308 (Low, F111 R8, unreachable defensive branch): `parse_diff_repair_response`
  returns `not_an_object` for a decoded value that is not a dict, and that
  branch cannot execute today: `extract_json_object` only ever returns text
  starting with `{`, so a successful `json.loads` always yields a dict. The
  worker disclosed it rather than writing a test that could not pass honestly,
  which is DECISION F105 D10 working as designed. Registered so the branch is
  never later mistaken for tested behaviour. It stays for now — it becomes
  reachable the moment `extract_json_object` learns to return array text — and
  the decision to keep or delete it belongs to the closure round, not to a
  repair. OPEN.
<<<LRG_END

4. C4 — ONE rewrite in `.agent/live_review.md`, nothing else in that file.
   The FROM line occurs EXACTLY 1x today; it is the last non-empty line of
   the file before C3's append. REWRITE (FROM and TO are disjoint).
   FROM (one line):
Landed: R-0307 — the live_review header no longer carries a finding-id counter, commit C4 of R8.
   TO (five lines), written to `.remedy-wt/f111r9/DONE` first and applied
   from that file:
Done: R-0307 — the header no longer names a next-free finding id; it points at
`.agent/plan.md`, which is rewritten every round and is the one place the
counter lives. Verified at the R8 gate: `sed -n '8,9p'` matches the authored
two-line replacement byte for byte, and the retired line is the single
deletion in commit ea0d63b3's `4 1` numstat. Resolved.
   In `git show --numstat <C4> -- .agent/live_review.md` the DELETE column
   must be exactly `1`; report the real insertion count.
   Commit: chore(f111): resolve R-0307 at the R8 gate   -> push

5. C5 — `packages/orchestration/review_scope.py`. Teach the EXISTING single
   walk to keep each file's raw diff lines, then expose them. No second
   parser, no second walk.
   (i) In `_parse_diff`, add `"lines": []` to the dict passed to
       `files.setdefault(...)`, alongside the existing keys. Every current
       consumer reads named keys only (`review_scope` lines 136 and 397,
       `pingpong_loop` line 1099), so this is additive.
   (ii) Capture the raw lines in that same walk:
        - track the `--- ` line itself in a `pending_old_line` variable
          (initialised `""` next to `pending_old_path`);
        - in the `+++ ` branch, after `current` is bound, append
          `pending_old_line` to `current["lines"]` ONLY if it is non-empty,
          then append the `+++ ` line, then reset `pending_old_line = ""`;
        - immediately after the `if current is None: continue` guard, and
          BEFORE the `@@` branch, append the raw line to `current["lines"]`
          so hunk headers, context lines, additions, removals and any
          "\ No newline at end of file" marker are all kept verbatim.
   (iii) Add a public
         `split_diff_by_path(diff_text: str) -> dict[str, str]` directly
         below `parse_diff_line_ranges`, returning
         `{path: "\n".join(info["lines"])}` over `_parse_diff(diff_text)`.
         One-line WHY comment directly above the definition (AGENTS.md Code
         Discoverability). Its docstring states: that it is the same single
         walk `parse_diff_line_ranges` uses; that a section runs from its
         `---`/`+++` header pair to the line before the next file header, so
         each value is a standalone diff the applicator can take on its own;
         that a path appearing twice in one diff gets its sections
         concatenated; and that any preamble before the first `---`
         (`diff --git`, `index`) belongs to no file and is dropped, because
         the applicator reads hunk headers and body lines only.
   Add tests to `tests/orchestration/test_review_scope.py` covering at least:
   a single-file diff round trip; a two-file diff where each returned section
   starts with its own `--- ` line and does NOT contain the other file's path;
   a diff carrying `diff --git` and `index` preamble lines, asserting they are
   absent from every section; the same path appearing twice, asserting both
   hunk headers survive in one section; an empty string in, `{}` out; and that
   `parse_diff_line_ranges` returns exactly what it returned before for the
   same two-file input, so the added key changed no existing reading.
   Commit: feat(f111): split a unified diff into per path sections -> push

6. C6 — `packages/orchestration/diff_repair_response.py` plus tests in
   `tests/orchestration/test_diff_repair_response.py`, in ONE commit.
   (i) Add `diff_repair_response_to_patch(response: DiffRepairResponse)
       -> StructuredPatch`, built on `review_scope.split_diff_by_path`. One
       `structured_patch.UnifiedDiff` per DECLARED path, in
       `response.files` order, each carrying ONLY that path's section;
       `intent_kind="unified_diff"`, `target_paths=tuple(response.files)`,
       `applicability="applicable"`, `requires_approval=True`.
       A declared path with no section gets an EMPTY diff string on purpose:
       `structured_patch.validate_structured_patch` then rejects it with
       `unified_diff <path>: empty diff`, so the failure is fail-closed and
       named instead of a silent no-op apply. The docstring says exactly that,
       and says callers run `validate_diff_repair_response` FIRST. One-line
       WHY comment directly above the definition.
   (ii) REWRITE the module-docstring paragraph that declares the conversion
        absent. FROM occurs EXACTLY 1x (it is lines 24-29 of the file today):
Remedy deliberately does not convert a ``DiffRepairResponse`` into a
``StructuredPatch`` in this half. ``structured_patch.UnifiedDiff`` pairs ONE
path with ONE diff text, so a ``files`` list longer than one entry has no
correct conversion yet — handing every declared path the whole diff would try to
apply every hunk to every file. The per-path diff split is designed together
with the apply half (R9), and the conversion lands there.
        TO (seven lines), written to `.remedy-wt/f111r9/DOC` first and applied
        from that file:
``structured_patch.UnifiedDiff`` pairs ONE path with ONE diff text, so a
``files`` list longer than one entry is split per path before conversion:
handing every declared path the whole diff would try to apply every hunk to
every file. The splitter is ``review_scope.split_diff_by_path``, the same
single walk that reads hunk headers. Remedy deliberately does not APPLY the
converted patch from this module — the apply-and-fallback half attaches to the
bridge, where the job, the approved intent and the snapshot already live.
   (iii) Add to the `Public API::` block, on its own line, directly below the
         `validate_diff_repair_response(response) -> list[str]` line:
    diff_repair_response_to_patch(response) -> StructuredPatch
   Tests to add, each its own test: a single-file response converts to one
   `UnifiedDiff` whose path and section are right and whose `intent_kind`,
   `target_paths`, `applicability` and `requires_approval` are as specified;
   a two-file response yields two entries, each containing only its own path;
   a declared path the diff never touches yields an empty diff string AND
   `validate_structured_patch` on the converted patch reports exactly
   `unified_diff <path>: empty diff`; and a valid response converts to a patch
   `validate_structured_patch` accepts with `[]`.
   Commit: feat(f111): convert a diff repair response to a patch -> push

7. C7 — `.agent/plan.md` FULL REPLACEMENT with the slice delimited by
   `<<<PLAN_BEGIN` and `<<<PLAN_END` (marker lines excluded). Write it to
   `.remedy-wt/f111r9/PLAN` first, then `cp .remedy-wt/f111r9/PLAN
   .agent/plan.md`; `cmp` silent. It is 46 lines — do not reflow it.
   Then rewrite `.agent/handoff.md` in YOUR OWN text. COUNT THE LINES BEFORE
   COMMITTING (`wc -l`): 60 or fewer, or carry a DECISION D15 "Deviations,
   declared" line naming the REAL measured count and the mandated content
   that caused it. Mandated content: feature and round (F111 R9); the branch;
   a per-commit SHA table for C1-C7 with insertions; a changed-files table;
   the real gate results below with commands and real exit codes; open
   findings 28 with next free id R-0309; an item-status table over C1-C7
   whose Status cells carry the SAME status you declare in the handback —
   `done`, `skipped` with reason, or `deviated` with reason (finding R-0306);
   this line verbatim, on its own line (finding R-0304):
Fortschritt: ~60 % (T001 ✅ · T002 fast: Record + Split ✅, Apply+Fallback offen · T003 offen) — Schätzung
   and a NEXT SESSION block stating, in this order: that the branch is
   UNMERGED and has NO PR by design; that the next action is R10, the apply
   and fallback half of T002; and that NOTHING imports `diff_repair.py` or
   `diff_repair_response.py` yet — both are seams and T003 wires them.
   Keep the handoff to mandated content: prose padding is a finding at any
   length (AGENTS.md, DECISION D15).
   plan.md and handoff.md land in ONE commit.
   Commit: chore(f111): rewrite the plan and handoff for R9   -> push

<<<PLAN_BEGIN
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged. Last reviewed SHA: 456a25e9 (R8 PASS). Next free finding
ID: R-0309. Open findings: 28, none above Medium.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
T002 is all but the apply, and still has NO CALL SITE. On disk in
`diff_repair_response.py`: the versioned `{format, version, diff,
files}` record, its parse, the validation that cross-checks the
declared `files` list against the paths the diff really touches,
`precheck_diff_repair_fences` — the non-raising fence decision that
rejects an out-of-fence path before the applicator — and now
`diff_repair_response_to_patch`, which converts a validated response
into the `StructuredPatch` the existing applicator already takes.
The per-path split it needs is `review_scope.split_diff_by_path`,
placed inside the module that owns hunk-header reading so no second
walk exists. Nothing imports any of it: T001 and T002 are seams.

## Next Steps
1. R10 — the apply half: run the converted patch through
   `apply_structured_patch` with its snapshot and approval gates, and
   on ANY hunk conflict discard the attempt whole, record
   `fallback_reason`, report mode `full_fallback`, and prove every
   touched file byte-identical to its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- `source_apply._apply_hunks` is the strict applier and must be
  reused, never duplicated. `review_scope` is now the only module
  that reads hunk headers OR splits a diff by path.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real, and until it lands the
  Fortschritt figure is about code written, not behaviour shipped.
<<<PLAN_END

Done when (record command + real exit code + counted value; never the word
"green"):
  a. `cmp .remedy-wt/f111r9/BLOCK .agent/authored/f111-r9-1.md` silent;
     `cmp .agent/authored/f111-r9-1.md .agent/last_block.md` silent;
     `cmp .remedy-wt/f111r9/PLAN .agent/plan.md` silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> delete column `0`;
     `git show --numstat <C4> -- .agent/live_review.md` -> delete column `1`.
     Report both real insertion counts.
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 33 ; `grep -c '^Done:'` -> 5
     `grep -c '^Landed:'` -> 0 (exit 1 is the pass)
     `grep -c '^### R8 — PASS'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r9/LRG').read_text()))"
     -> exit 0, printed count 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r9/DONE').read_text()))"
     -> exit 0, printed count 1
  d. on `.agent/plan.md`: `wc -l` -> 46 ; `grep -c '^## Goal'` -> 1 ;
     `grep -c '^## Next Steps'` -> 1 ; `grep -c 'R-0309'` -> 1.
     `wc -l < .agent/handoff.md` -> the real number, 60 or fewer unless the
     D15 line declares it; `grep -c '^Fortschritt: ' .agent/handoff.md` -> 1
  e. behaviour pin for C5 — the `_parse_diff` consumers this round does NOT
     touch: `python3 -m pytest tests/orchestration/test_final_verifier.py
     tests/orchestration/test_reviewer_prompt_scope.py
     tests/orchestration/test_pingpong.py -q` -> exit 0, 146 passed, the SAME
     count this reviewer measured at HEAD before the round.
  f. `python3 -m pytest tests/orchestration/test_review_scope.py -q` -> exit 0,
     at least 32 passed (32 is the pre-round count; report the real number).
     `python3 -m pytest tests/orchestration/test_diff_repair_response.py -q`
     -> exit 0, at least 23 passed; report the real number.
     `python3 -m pytest tests/orchestration/test_diff_repair.py -q` -> exit 0,
     30 passed, unchanged.
     `python3 -m pytest tests/cli/test_golden_path.py -q` -> exit 0, 42 passed
     (canary). Do NOT run tests/ui_server/test_dashboard_contract.py
     (R-0221: it runs a real npm build).
  g. `python3 -m pytest tests/test_path_utils.py tests/test_data_paths.py -q`
     -> exit 0, report the real count: these rglob every `packages/**/*.py`.
  h. red-proof, inside a DISPOSABLE `git worktree` at HEAD and nowhere else:
     in that worktree only, make `split_diff_by_path` return the WHOLE
     `diff_text` for every path instead of that path's section, run
     `python3 -m pytest tests/orchestration/test_review_scope.py
     tests/orchestration/test_diff_repair_response.py -q` and record the real
     exit code and the failing test ids; then remove and prune the worktree.
     If the mutation does NOT go red, say so plainly — a true report about an
     unreachable branch is worth more than a colour.
  i. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C7 with real statuses, raw gate
             results a-i with real exit codes) and `.agent/handoff.md`
             rewritten as C7. Do not merge, do not open a PR.
