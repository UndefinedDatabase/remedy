── STEP R12/6 — F111 Diff-only repair — SESSION CLOSE, R11 gate ──────────────
Goal:        Record the R11 PASS gate, resolve R-0312, register R-0315, and
             close the session. This round is the SESSION-CLOSING gate round
             and changes no production code. The apply-and-fallback half of
             T002 is R13 and is NOT in this round.
Bundle:      C1 block save; C2 last_block mirror; C3 gate + Done + finding;
             C4 plan and closing handoff. Commit AND push at every item.
Change:      EXACTLY these paths and nothing else:
             .agent/authored/f111-r12-1.md (new), .agent/last_block.md,
             .agent/live_review.md, .agent/plan.md, .agent/handoff.md.
Constraints: AGENTS.md in full. Apply every authored slice by READING ITS
             SCRATCH FILE (`cat` / `cp`) — never retype, never reflow.
             Do NOT touch `.agent/candidates.md`, `.agent/context.md` or
             `.agent/decisions.md`. Touch NO file under `packages/`, `tests/`
             or `docs/`: this round records a verdict, it does not change
             behaviour, and widening the change set is scope drift.
             Write no `Done:` line of your own: only reviewer-authored text
             sets Resolved (docs/agents/planner_reviewer_prompt.md §4.4). This
             round orders NO `Landed:` line, because it fixes nothing.
             This is the LAST round of the session — after C4, stop and hand
             back. Do not start R13.

PROCEDURE (in order; commit AND push at every numbered item):

0. Preconditions: `git status --porcelain` empty; branch is
   feature/f111-diff-only-repair; `git log -1 --format=%h` is 06e85a11.
   Any mismatch => STOP and hand back.  `mkdir -p .remedy-wt/f111r12`.

1. C1 — Save this ENTIRE step block (from the `── STEP R12/6` line through the
   final `Handback:` line, byte for byte) to `.remedy-wt/f111r12/BLOCK`, then
   `cp .remedy-wt/f111r12/BLOCK .agent/authored/f111-r12-1.md`; `cmp` silent.
   Commit: chore(f111): save the R12 step block verbatim   -> push

2. C2 — `cp .agent/authored/f111-r12-1.md .agent/last_block.md`; `cmp` silent.
   Commit: chore(f111): mirror the R12 block into last block   -> push

3. C3 — FINDINGS FIRST, two operations on `.agent/live_review.md`:
   (a) DELETE its LAST line — the R-0312 `Landed:` line, which the reviewer now
       replaces with authored `Done:` text (§4.4). It is the final line of the
       file; remove that one line and nothing else.
   (b) Write the slice delimited by `<<<LRG_BEGIN` and `<<<LRG_END` (marker
       lines excluded) to `.remedy-wt/f111r12/LRG`, then
       `cat .remedy-wt/f111r12/LRG >> .agent/live_review.md`.
   In `git show --numstat <C3> -- .agent/live_review.md` the DELETE column must
   be exactly `1`; report the real insertion count.
   Commit: chore(f111): record the R11 gate and finding R-0315   -> push

<<<LRG_BEGIN
### R11 — PASS (2026-08-13)
Reviewed by the main session over 8644def9..06e85a11. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: PRIMARY cmp proof — `.agent/authored/f111-r11-1.md` and
`.agent/last_block.md` are byte-identical. Numstat purity: `102 1` for the gate
commit, the single deletion being the retired R-0311 marker line the reviewer
replaced with authored text, and `2 0` for the new marker line. Markers on the
final file: 39 registered ids, 6 resolutions, 1 landed marker, 1 R10 pass
heading, 1 D5 heading. Scope: exactly the seven ordered paths, no more.

The fix proved BY VALUE, not by colour. Against `'a\nb\nc\n'`, the reviewer ran
the three zero-count headers real `git diff -U0` emits for an insert-in-middle,
a prepend and an append: `@@ -1,0 +2 @@`, `@@ -0,0 +1 @@` and `@@ -3,0 +4 @@`,
each with a single `+X` body. They now return `'a\nX\nb\nc\n'`, `'X\na\nb\nc\n'`
and `'a\nb\nc\nX\n'`. On the R10 applier the same three returned
`'X\na\nb\nc\n'`, `'a\nb\nc\nX\n'` and `'a\nb\nX\nc\n'` — every one placed
wrong, and the prepend silently appended. Both rejections were exercised
directly: `@@ -0,1 +0,2 @@\n+X\n` on `'a\nb\n'` returned `'a\nb\nX\n'` before
and returns None now, and `@@ -1,0 +2 @@\n a\n+X\n` on `'a\na\nb\n'` — chosen
because its context line still MATCHES at the shifted index, so only the new
contradiction check can reject it — returns None. R10's own fix still holds:
the `alpha/BETA/gamma` probe still prints `'alpha\nBETA\ngamma\n'`.

Tests, each re-run by the reviewer: 185 passed for the source-apply tier, 179
before the round plus the 6 new cases; 138 for the untouched modules plus the
golden-path canary, unchanged; 225 for the applier's other consumers,
unchanged, so the header change regressed no existing consumer. Red-proof: in a
disposable worktree at HEAD with `source_apply.py` checked out from 8644def9 —
which reverts exactly C4 and nothing else —
`pytest tests/orchestration/test_source_apply_transaction.py -q` exited 1 with
6 failed / 15 passed, the six failures being exactly the six tests C4 adds,
with every pre-existing test still passing on the old applier. Worktree removed
and pruned; `git status --porcelain` empty, `git worktree list` one entry,
`git rev-list --left-right --count` against the remote `0 0`. Caps: per-commit
insertions 355/266/102/71/2/99, each under 500; `.agent/plan.md` 49 lines,
under the AGENTS.md limit of 50; `.agent/handoff.md` 95 lines, over the 60 cap
and carrying the DECISION D15 stated-cause line, which is the sanctioned shape.
No deviations were declared and the reviewer found none.

Done: R-0312 — a hunk whose OLD COUNT is 0 now splices AFTER the line its
header names instead of one line before it, so a pure-insertion hunk lands
where the diff says and `@@ -0,0 +1 @@` prepends instead of silently appending.
A header that declares a pure insertion while its body consumes original lines
is rejected outright, and a negative splice index can no longer be reached. The
absent-count short form `@@ -2 +1,0 @@` still means a count of 1 and is
unchanged. Proved by value at the R11 gate in both directions and pinned by six
new tests, all six of which fail on the pre-fix applier. Resolved.

With R-0311 and R-0312 both closed, `_apply_hunks` places a hunk's content
correctly in both axes it can get wrong: WHERE inside the hunk an added line
goes, and WHERE in the file the hunk itself starts. Remedy deliberately does
not cross-check a hunk header's declared old count against the number of lines
its body actually consumes when that count is 1 or more: models routinely
miscount headers while quoting content exactly, and this applier's strictness
is deliberately spent on CONTENT — every context and removal line is compared
against the real file — rather than on arithmetic a wrong-but-harmless header
would fail. The count is read only to decide the zero-insertion case, where it
is the sole available signal.

- R-0315 (Medium, F111 R11, feature file allows what the applicator refuses):
  `docs/roadmap/features/T2_F111.md` states under "Edge cases & assumption
  defaults (A9)" that new-file creation inside a diff is ALLOWED if the path
  passes fences, and that only deletions require the full-file path in v1. The
  code disagrees: `_apply_unified_diff` returns early with
  `f"{diff.path}: file not found for diff"` and sets `success = False` whenever
  `full.is_file()` is false, so a diff that creates a file can never apply, and
  a model that correctly answers a repair with a new-file hunk gets a failed
  apply rather than a created file. Found by the reviewer while gating R11, not
  by a test. Note the interaction with R-0312: a new-file diff is exactly the
  `@@ -0,0 +1,N @@` shape whose placement R11 just fixed, so the two would meet
  in the same code path the moment the file-existence guard is lifted. This is
  NOT a defect R11 introduced and NOT one R11 should have fixed — its change
  set was the header computation — but T002's apply half runs straight into it,
  so it is registered before that round rather than discovered during it. R13
  decides: either implement creation behind the fence check as the feature file
  says, or amend the feature file to match v1 reality under §4.7 and say why.
  Do not let R13 pick silently. OPEN.
<<<LRG_END

4. C4 — `.agent/plan.md` FULL REPLACEMENT with the slice delimited by
   `<<<PLAN_BEGIN` and `<<<PLAN_END` (marker lines excluded). Write it to
   `.remedy-wt/f111r12/PLAN` first, then `cp .remedy-wt/f111r12/PLAN
   .agent/plan.md`; `cmp` silent. Do NOT gate it on a line count and do NOT
   reflow it: the `cmp` is the proof (finding R-0309).
   Then rewrite `.agent/handoff.md` in YOUR OWN text as the SESSION-CLOSING
   handoff. COUNT THE LINES BEFORE COMMITTING (`wc -l`): 60 or fewer, or carry
   a DECISION D15 "Deviations, declared" line naming the REAL measured count
   and the mandated content that caused it. Mandated content: feature and round
   (F111 R12, SESSION CLOSE); the branch; a per-commit SHA table for C1-C4 with
   insertions; a changed-files table; the real gate results a-f with commands
   and real exit codes; open findings 33 with next free id R-0316; an
   item-status table over C1-C4 whose Status cells carry the SAME status you
   declare in the handback (finding R-0306); this line verbatim, on its own
   line (finding R-0304):
Fortschritt: ~62 % (T001 ✅ · T002: Record + Split ✅, Apply+Fallback offen · T003 offen · Applier-Fixes R-0311 + R-0312 ✅) — Schätzung
   and a NEXT SESSION block stating, in this order: that the branch is UNMERGED
   and has NO PR by design, so the Open PR Gate does not apply and Phase 0 must
   sweep `feature/*` branches (finding R-0290) to see it; that this session
   gated R10 and R11 and closed both halves of the applier placement defect,
   R-0311 in-body and R-0312 header-side; that R12 is the session-closing gate
   round and, per docs/agents/planner_reviewer_prompt.md §4.13, the LAST round
   of a branch has no on-disk gate entry by construction, so the next session
   must NOT open a repair round to close R12 — its verdict lives in this
   handoff; that the next action is R13, the apply-and-fallback half of T002,
   which must first settle R-0315 (new-file creation: implement it behind the
   fence check or amend the feature file under §4.7, but not silently); that
   R-0313 is open BY DECISION and its normalisation belongs on the response
   side in T002/T003, not in the applier; and that NOTHING imports
   `diff_repair.py` or `diff_repair_response.py` yet — both are seams, T003
   wires them, and a green suite over an unreferenced module is not a working
   feature. Keep to mandated content: prose padding is a finding at any length
   (AGENTS.md, DECISION D15).
   plan.md and handoff.md land in ONE commit.
   Commit: chore(f111): write the session closing handoff   -> push

<<<PLAN_BEGIN
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 06e85a11 (R11 PASS).
Next free finding ID: R-0316. Open findings: 33, measured on disk as
40 registered minus 7 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R12 is the session-closing gate round: it records the R11 verdict,
resolves R-0312 and registers R-0315. Both halves of the applier's
placement defect are now closed — R-0311 fixed WHERE an added line
lands inside its hunk, R-0312 fixed WHERE the hunk itself starts.
T002 otherwise stands at record, validation, fence pre-check, split
and conversion — all on disk, all still WITHOUT a call site.

## Next Steps
1. R13 — the apply half of T002. Settle R-0315 FIRST: the feature
   file allows new-file creation inside a diff, the applicator
   rejects any diff whose target file does not exist. Then run a
   converted patch through `apply_structured_patch`, and on ANY hunk
   conflict discard the attempt whole, record `fallback_reason`,
   report mode `full_fallback`, and prove every touched file
   byte-identical to its pre-attempt state.
2. T003 — wire `changed_line_ranges_from_patch` and the response
   channel into `run_builder_bridge_loop`, emit mode and token
   evidence per repair round, add the fixture token comparison.
3. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0313 is open by decision: a blank context line stripped to ""
  makes a diff REJECT where the pre-R10 applier applied it. Safe
  direction; the normalisation belongs on the response side.
- `source_apply._apply_hunks` is the only applier and `review_scope`
  the only diff reader. Neither may be duplicated.
- A green suite over unreferenced modules is not a working feature.
  T003 is the round that makes F111 real.
<<<PLAN_END

Done when (record command + real exit code + counted value; never the word
"green"):
  a. `cmp .remedy-wt/f111r12/BLOCK .agent/authored/f111-r12-1.md` silent;
     `cmp .agent/authored/f111-r12-1.md .agent/last_block.md` silent;
     `cmp .remedy-wt/f111r12/PLAN .agent/plan.md` silent.
  b. `git show --numstat <C3> -- .agent/live_review.md` -> delete column `1`.
     Report the real insertion count.
  c. on the final `.agent/live_review.md`:
     `grep -c '^- R-0'` -> 40 ; `grep -c '^Done:'` -> 7
     `grep -c '^Landed:'` -> 0 (grep exits 1 when it prints 0; that IS the
     pass, since this round fixes nothing and retires the previous marker)
     `grep -c '^### R11 — PASS'` -> 1
     python3 -c "import pathlib;print(pathlib.Path('.agent/live_review.md').read_text().count(pathlib.Path('.remedy-wt/f111r12/LRG').read_text()))"
     -> exit 0, printed count 1
  d. `grep -c '^## Goal' .agent/plan.md` -> 1 ;
     `grep -c '^## Next Steps' .agent/plan.md` -> 1 ;
     `grep -c 'R-0316' .agent/plan.md` -> 1 ; report `wc -l` as a fact, not as
     a gate. `wc -l < .agent/handoff.md` -> the real number, 60 or fewer unless
     the D15 line declares it; `grep -c '^Fortschritt: ' .agent/handoff.md` -> 1
  e. NOTHING outside `.agent/` changed:
     `git diff --name-only 06e85a11..HEAD` -> exactly five paths, all under
     `.agent/`. Paste the real list.
     The applier is untouched, so re-run the two value probes and paste their
     real output; both must be unchanged from the R11 gate:
     python3 -c "from packages.orchestration.source_apply import _apply_hunks as A; print(repr(A('a\nb\nc\n','@@ -1,0 +2 @@\n+X\n')), repr(A('alpha\nbeta\ngamma\n','@@ -1,3 +1,3 @@\n alpha\n-beta\n+BETA\n gamma\n')))"
     -> exit 0, printed 'a\nX\nb\nc\n' 'alpha\nBETA\ngamma\n'
     `python3 -m pytest tests/orchestration/test_source_apply_transaction.py
     tests/cli/test_golden_path.py -q` -> exit 0, 63 passed (21 + 42 canary).
     Do NOT run tests/ui_server/test_dashboard_contract.py (R-0221: it runs a
     real npm build).
  f. `git status --porcelain` -> empty; `git worktree list` -> one entry;
     per-commit insertions each < 500;
     `git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD`
     -> `0 0` after the final push.
Handback:    completion report (per-commit table, changed-files table,
             item-status table over C1-C4 with real statuses, raw gate results
             a-f with real exit codes) and `.agent/handoff.md` rewritten as C4.
             Do not merge, do not open a PR, do not start R13.
