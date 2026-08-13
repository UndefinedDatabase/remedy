── STEP T002-close / F111 — Round 14 ──────────────────────────────
Goal:
  Record the R13 verdict, resolve R-0315, register R-0316, then close R-0313 on
  the RESPONSE side: a blank context line that lost its leading space in
  transport must stop making a valid diff reject.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r14-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md bookkeeping, all three edits in ONE commit:
      apply PAIR-L, then append TEXT-F, then append TEXT-G
  C4  normalize_diff_blank_context + its call site, in
      packages/orchestration/diff_repair_response.py
  C5  tests: four cases in tests/orchestration/test_diff_repair_response.py and
      one end-to-end case in tests/orchestration/test_diff_repair_apply.py
  C6  replace .agent/plan.md with TEXT-D, then rewrite .agent/handoff.md

Change — C4, the ONLY production commit of this round:
  In packages/orchestration/diff_repair_response.py add ONE public function:

    def normalize_diff_blank_context(diff_text: str) -> str

  What it fixes (finding R-0313, measured on this machine at the R14 gate):
  against the file 'a\n\nb\n', the diff "@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n"
  returns None, while the same diff with the blank line written as a single
  space returns 'a\n\nB\n'. A model or a transport that strips the trailing
  space off a blank context line therefore turns a correct answer into a
  fallback. The applier is RIGHT to reject it — the fix belongs here, where the
  diff's own hunk structure is known.

  Algorithm, exactly:
  1. lines = diff_text.splitlines(). Use splitlines(), NEVER split("\n").
     This is load-bearing, not style: split("\n") appends a phantom "" for any
     diff ending in a newline, and converting that phantom to " " would append
     a stray context line to the last hunk. splitlines() drops the phantom and
     keeps every genuine blank line, so the trap cannot be reached.
  2. Walk the lines with a hunk budget. On a header matching
     ^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@ set old_remaining to the old
     count and new_remaining to the new count (an absent count means 1), and
     mark that a hunk is open.
  3. While a hunk is open: a line starting with " " decrements both counters; a
     line starting with "-" decrements old_remaining; a line starting with "+"
     decrements new_remaining; a line starting with "---", "+++" or "diff "
     closes the hunk and is emitted unchanged; any other line (in practice
     "\ No newline at end of file") is emitted unchanged and decrements
     nothing.
  4. The one rewrite: a line that is EXACTLY "" while a hunk is open AND
     old_remaining > 0 AND new_remaining > 0 is a blank context line that lost
     its space. Emit " " and decrement both counters. A "" line in any other
     position — outside a hunk, or after the hunk's budget is spent — is
     emitted unchanged.
  5. Join with "\n"; if diff_text ended with "\n", re-append it, so the
     function is byte-identity on any diff that needs no repair.

  Call site: `diff_repair_response_to_patch` normalises FIRST and splits the
  NORMALISED text —
      sections = split_diff_by_path(normalize_diff_blank_context(response.diff))
  and nothing else in that function changes. `validate_diff_repair_response`
  keeps reading the RAW diff: blank body lines do not affect the header parse,
  and validation must judge what the model actually sent.

  Docstrings: give the new function the module's voice — what a stripped blank
  context line is, why the repair cannot live in `_apply_hunks` (a trailing ""
  from `split("\n")` would make the last hunk consume one original line too
  many, trading a safe rejection for a silent corruption), and the deliberate
  absence: a diff whose FINAL line is a blank context line and which does not
  end in a newline is left alone, because nothing distinguishes it from a
  truncated body — the safe direction is the existing rejection. Add the new
  function to the module docstring's "Public API::" list. Carry the one-line
  WHY comment above the definition, as the sibling functions do.

Change — C5, tests:
  In tests/orchestration/test_diff_repair_response.py add FOUR cases for
  normalize_diff_blank_context, in the file's existing style:
  1. a blank context line inside a hunk regains its space:
     "@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n" becomes
     "@@ -1,3 +1,3 @@\n a\n \n-b\n+B\n".
  2. identity on a diff that needs no repair: assert
     normalize_diff_blank_context(DIFF_ONE_FILE) == DIFF_ONE_FILE, the exact
     byte-identity that proves step 5 and protects the existing assertion
     `only.diff == DIFF_ONE_FILE.rstrip("\n")` in this same file.
  3. a blank line BETWEEN two file sections is untouched: build the input from
     DIFF_ONE_FILE + "\n" + the second file section of DIFF_TWO_FILES and
     assert the output equals the input.
  4. the budget is respected: in "@@ -1,2 +1,2 @@\n a\n-b\n+B\n" the hunk's
     counters reach zero at "+B", so a "" AFTER it stays "". Assert the
     trailing blank is still "" in the output.

  In tests/orchestration/test_diff_repair_apply.py add ONE end-to-end case,
  reusing that file's _make_approved_job scaffolding:
  5. a stripped blank context line now LANDS instead of falling back. repo/c.py
     = "a\n\nb\n"; response diff
     "--- a/c.py\n+++ b/c.py\n@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n" with
     files ("c.py",). Assert mode == DIFF_REPAIR_MODE_DIFF, applied is True,
     and (repo/"c.py").read_text() == "a\n\nB\n". Name it for R-0313 and say in
     its docstring that this exact input returned mode full_fallback before the
     normaliser existed.

Constraints:
  - AGENTS.md in full: self-review loop before every commit, one logical step
    per commit, <500 INSERTIONS per commit, plan.md current before committing,
    clean tree, push after every commit.
  - The change set is EXACTLY these eight paths and nothing else:
    .agent/authored/f111-r14-1.md, .agent/last_block.md, .agent/live_review.md,
    packages/orchestration/diff_repair_response.py,
    tests/orchestration/test_diff_repair_response.py,
    tests/orchestration/test_diff_repair_apply.py, .agent/plan.md,
    .agent/handoff.md. Touching any other path is a scope violation — report it
    instead of doing it.
  - Do NOT modify packages/orchestration/source_apply.py. R-0313 is fixed on
    the response side by decision; `_apply_hunks` stays as it is.
  - Do NOT modify packages/orchestration/diff_repair_apply.py. R-0316 is
    registered in this round and FIXED in R15, where T003 emits the field.
  - Do NOT add a call site for apply_diff_repair; R15 owns the wiring.
  - Do NOT write any `Done:` paragraph of your own. TEXT-F and the PAIR-L TO
    are reviewer-authored; apply them verbatim and add nothing
    (planner_reviewer_prompt.md §4.4).
  - Never force-push, never work on main, never merge.

PAIR-L — .agent/live_review.md, a REWRITE (the TO does not contain the FROM).
These two lines are currently the LAST two lines of the file.
FROM (2 lines, exact):
Landed: R-0315 — T2_F111.md A9 sentence rewritten and the D6 Built State
section appended; the applicator guard is unchanged by decision.
TO (9 lines, exact):
Done: R-0315 — the feature file no longer allows what the applicator refuses.
DECISION F111 D6 keeps `_apply_unified_diff`'s file-existence guard and amends
the A9 sentence instead, so creation and deletion now take the same full-file
route in v1. Verified at the R13 gate BY VALUE: a `--- /dev/null` answer with
`@@ -0,0 +1,2 @@` returns mode `full_fallback` and `fallback_reason` exactly
`apply_failed:new.py: file not found for diff`, with no file created — so the
mechanism that fires is the guard the amended A9 sentence names, not a snapshot
block, which would have made that text wrong. Pinned by test_diff_repair_apply
::test_new_file_creation_diff_falls_back_instead_of_creating. Resolved.

TEXT-F — append verbatim to the END of .agent/live_review.md (commit C3),
after PAIR-L has been applied:
- R-0316 (Medium, F111 R13, a fallback reports a clean tree it cannot
  guarantee): `diff_repair_apply.apply_diff_repair` returns `files_modified=0`
  on every `apply_failed:` path, and its docstring states that the durable
  snapshot restores "every touched file when a hunk conflicts". Both hold only
  while the rollback SUCCEEDS. `source_apply._rollback_from_snapshot` catches
  OSError per entry and, when a blob cannot be read or a target cannot be
  written, appends `rollback_incomplete (N file(s)): …` to the errors and
  leaves those files half-restored; `result.success` is already False, so
  nothing else marks the difference. A caller then reads `applied=False,
  files_modified=0` and concludes the tree is untouched while it is not —
  the exact failure class this feature's Done criterion names. The information
  is not lost, the string rides in `errors`, but the summary field contradicts
  it and T003 will emit that field as per-round evidence. Reviewer-caused: the
  R13 step block ordered `files_modified=0` unconditionally, so this is a
  defect of the spec, not of the round that executed it faithfully. Fix
  direction: carry the rollback outcome as its own field, or refuse to zero
  `files_modified` when an error names `rollback_incomplete` — never by
  widening `_apply_hunks`. OPEN.

TEXT-G — append verbatim to the END of .agent/live_review.md (commit C3),
after TEXT-F:
### R13 — PASS (2026-08-13)
Reviewed by the main session over 34319061..9a17fad2. Every ordered gate was
re-run by the reviewer on this machine; nothing was read off the handback.
Transport: the worker's permission layer refused `cmp` and refused every
command naming `.remedy-wt/`, so it declared the gap instead of faking a result
and the reviewer ran the comparison itself. `.remedy-wt/f111r13/BLOCK`,
`.agent/authored/f111-r13-1.md` and `.agent/last_block.md` are all three
byte-identical at 18502 bytes, sha256
f35907a250068b81c3c5b6216b2fcd68220674d997aadb40d3ce869fadc622f0;
`.remedy-wt/f111r13/PLAN` and `.agent/plan.md` identical at 2124 bytes. Both
authored appends landed verbatim and exactly once each. Scope: exactly the nine
ordered paths, `source_apply.py` untouched, R-0313 untouched, and no call site
added — `grep -rn diff_repair_apply packages/ apps/` returns one line, the
docstring pointer.

The all-or-nothing claim proved BY MUTATION, not by colour. In a disposable
worktree at HEAD the reviewer replaced the body of `_rollback_from_snapshot`
with an immediate `return` and re-ran the new test file:
`test_conflicting_hunk_falls_back_and_leaves_both_files_untouched` FAILED with
`assert b'LINE1\nline2\n' == b'line1\nline2\n'` while the other five passed. So
the first file really is written before the second hunk conflicts, and the
rollback really is what restores it — the test is load-bearing, not vacuously
green. Worktree removed and pruned before this verdict.

DECISION D6 was checked against behaviour rather than against its own prose: a
creation diff returns `apply_failed:new.py: file not found for diff` with a
non-empty snapshot id and no file created, so the guard the amended A9 sentence
names is the mechanism that actually fires.

Tests, each re-run by the reviewer: 54 for the three scoped files, 294 for
tests/docs/ (the docs-round gate this change set requires), 42 for the
golden-path canary. Markers: 1 D6 heading, 1 landed marker, `Done:` still 7 on
the file the round handed back. Caps: per-commit insertions
320/299/18/19/174/262/108, each under 500; `.agent/plan.md` 43 lines under the
50 cap; `.agent/handoff.md` 109 lines over the 60 cap and carrying the DECISION
D15 stated-cause line, which is the sanctioned shape. `git status --porcelain`
empty, one worktree, `0	0` against the remote. The handback stated C7's own
insertions as a bound rather than a count, twice and with two different bounds
(`≤148` and "at most 152"); both are true of the real 108 and neither is a
false claim, so it is noted here and not registered. One finding registered:
R-0316, and it is the reviewer's own spec defect, not the worker's.

TEXT-D — the COMPLETE new content of .agent/plan.md (commit C6). Replace the
file; do not merge with what is there:
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 9a17fad2 (R13 PASS).
Next free finding ID: R-0317. Open findings: 33 — 41 registered minus
8 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R14 closes R-0313 on the response side: a blank context line whose
single leading space was stripped in transport arrives as "" and makes
an otherwise valid diff REJECT. `normalize_diff_blank_context` restores
the space while the hunk's own line budget says the line is still body,
so the diff reaches the applicator intact. T002 is otherwise complete:
record, split, schema, fence pre-check and the apply-and-fallback seam.

## Next Steps
1. R15 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison. R15 also fixes R-0316,
   because it is T003 that emits `files_modified` as evidence.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- R-0316 is open: a failed rollback leaves files changed while the
  seam still reports `files_modified=0`. Narrow (OSError during
  restore) but it is the Done criterion's own failure class.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.
- A green suite over unreferenced modules is not a working feature.
  R15 is the round that makes F111 real.

Done when — run every command, record the REAL exit code and the REAL counted
value for each. "Green" as a word is a finding.
  a. sha256sum .agent/authored/f111-r14-1.md .agent/last_block.md -> exit 0,
     the two digests identical. (The reviewer runs the cmp against its own
     originals; do not attempt to read `.remedy-wt/`.)
  b. on .agent/live_review.md:
     grep -c '^Landed:' -> prints 0, exit 1 (that is the pass).
     grep -c '^Done:' -> 8.
     grep -c '^- R-0' -> 41.
     grep -c '^### R13 — PASS' -> 1.
  c. grep -c 'def normalize_diff_blank_context' packages/orchestration/diff_repair_response.py
     -> 1.
     grep -c 'split_diff_by_path(normalize_diff_blank_context' packages/orchestration/diff_repair_response.py
     -> 1.
  d. VALUE PROBE, run it and paste the real output:
     python3 -c "from packages.orchestration.diff_repair_response import
     normalize_diff_blank_context as n;
     print(repr(n('@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n')))"
     -> must print '@@ -1,3 +1,3 @@\n a\n \n-b\n+B\n'.
  e. VALUE PROBE, the R-0313 case end to end:
     python3 -c "from packages.orchestration.diff_repair_response import
     normalize_diff_blank_context as n;
     from packages.orchestration.source_apply import _apply_hunks;
     print(repr(_apply_hunks('a\n\nb\n', n('@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n'))))"
     -> must print 'a\n\nB\n'. Before this round the same call without n()
     printed None.
  f. python3 -m pytest tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_diff_repair_apply.py
     tests/orchestration/test_diff_repair.py -q -> exit 0. Record the count.
  g. python3 -m pytest tests/orchestration/test_source_apply.py
     tests/orchestration/test_source_apply_transaction.py -q -> exit 0.
     Record the count. The applier is untouched, so this number must not move.
  h. python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0, canary.
     Record the count.
  i. git status --porcelain -> empty.
     git diff --name-only 9a17fad2..HEAD -> exactly the eight paths listed
     under Constraints, no others.
     git show --stat <sha> for EVERY commit -> each insertion count under 500;
     report the numbers.
     git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD
     -> 0	0 after the final push.

Handback: completion report + rewrite .agent/handoff.md per AGENTS.md
(feature + round, branch, per-commit table with insertion counts, changed-files
table, the a-i gate results with real exit codes and counted values, open
findings count, item-status table covering C1-C6 exactly once each, next
expected action). Repeat this Fortschritt line verbatim in the handoff:
Fortschritt: ~72 % (T001 ✅ · T002 ✅ komplett · T003 offen · R-0315 ✅ · R-0313 ✅ · R-0316 offen für R15) — Schätzung
──────────────────────────────────────────────────────────────
