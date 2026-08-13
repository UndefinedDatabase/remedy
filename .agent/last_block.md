── STEP T002-repair / F111 — Round 15 (SESSION CLOSING) ───────────
Goal:
  Record the R14 verdict, resolve R-0313, register R-0317, then repair the two
  reviewer-caused spec defects in T002 — the separator-eating normaliser
  (R-0317) and the fallback that reports a clean tree it cannot guarantee
  (R-0316) — so T003 starts from a seam that is honest in both directions.

Bundle (ordered; one commit each, push after EVERY commit per R-0289):
  C1  save this block verbatim to .agent/authored/f111-r15-1.md
  C2  mirror the same bytes into .agent/last_block.md
  C3  .agent/live_review.md bookkeeping, all three appends in ONE commit, in
      this order: TEXT-A, then TEXT-F, then TEXT-G
  C4  R-0317 fix + the comment typo, in
      packages/orchestration/diff_repair_response.py
  C5  tests for R-0317, in tests/orchestration/test_diff_repair_response.py and
      tests/orchestration/test_diff_repair_apply.py
  C6  R-0316 fix + its test, in packages/orchestration/diff_repair_apply.py and
      tests/orchestration/test_diff_repair_apply.py
  C7  replace .agent/plan.md with TEXT-D, then rewrite .agent/handoff.md

Change — C4, packages/orchestration/diff_repair_response.py:
  R-0317: a bare "" is hunk body ONLY when the next NON-BLANK line is also
  body. Today the budget alone decides, so a model that over-declares its hunk
  counts leaves budget unspent and the blank line SEPARATING TWO FILE SECTIONS
  becomes " " — measured at the R15 gate on this repository's own
  `DIFF_ONE_FILE` shape, where the normalised first section then returns None
  against a file that continues past the hunk while the raw section applies.

  Add one private helper next to the normaliser:

    def _blank_line_is_hunk_body(lines: list[str], start: int) -> bool

  It scans `lines` from `start` for the first entry that is not "", and returns
  False when there is none (end of input) or when that entry starts with
  "---", "+++" or "diff "; True otherwise. Scanning PAST consecutive blanks is
  deliberate: two blank context lines in a row are ordinary, and the run is
  classified by what follows it, not by its own length.

  In `normalize_diff_blank_context`, iterate with `enumerate` and extend the
  one rewrite branch — it fires only when the line is exactly "", a hunk is
  open, `old_remaining > 0`, `new_remaining > 0`, AND
  `_blank_line_is_hunk_body(lines, index + 1)`. Everything else in the
  function, including the `splitlines()` walk and the trailing-newline restore,
  is unchanged.

  Extend the function docstring: the budget alone is not sufficient because a
  hunk header may declare more lines than its body spends, and this repository
  treats that as routine (see the D5 note in `.agent/live_review.md` on why the
  applier does not cross-check declared counts against consumed ones); the
  lookahead is what keeps a file separator and an end-of-input blank out of the
  rewrite. Name R-0317 in that paragraph.

  Same commit, the comment typo the R14 handback reported: the `#` comment
  above the fall-through branch writes `"\\ No newline at end of file"` with a
  doubled backslash. A comment is not escape-processed, so make it a single
  backslash, matching packages/orchestration/source_apply.py. Do NOT touch the
  doubled backslashes inside the DOCSTRING (`split("\\n")`, `"\\ No newline"`):
  those are correct and required there.

Change — C5, tests for R-0317:
  In tests/orchestration/test_diff_repair_response.py, REPLACE the body of
  `test_blank_line_between_two_file_sections_is_untouched` with the form the
  R14 block originally ordered and which the fix now makes true: build the
  input as `DIFF_ONE_FILE + "\n" + <the second file section of
  DIFF_TWO_FILES>` and assert the output equals the input. Replace its
  docstring's deviation paragraph with one sentence naming R-0317: the shared
  constant declares `@@ -1,3 +1,3 @@` over a body that spends two old and two
  new lines, so it is exactly the over-declared shape that used to convert the
  separator, and asserting identity on it is the regression pin. Keep the class
  and the test name.

  Add ONE case to the same class: a blank line with unspent budget at END OF
  INPUT stays "". Use "@@ -1,3 +1,3 @@\n a\n-b\n+B\n\n" and assert the output
  equals the input.

  In tests/orchestration/test_diff_repair_apply.py add ONE end-to-end case,
  reusing `_make_approved_job`: a two-file answer whose first file CONTINUES
  past its hunk now lands. repo/app.py = "import os\nvalue = 1\nmore = 3\n",
  repo/util.py = "helper = 1\n". Response diff, exactly:
     "--- a/app.py\n+++ b/app.py\n@@ -1,3 +1,3 @@\n import os\n-value = 1\n"
     "+value = 2\n\n--- a/util.py\n+++ b/util.py\n@@ -1,1 +1,1 @@\n"
     "-helper = 1\n+helper = 2\n"
  files ("app.py", "util.py"). Assert mode == DIFF_REPAIR_MODE_DIFF, applied is
  True, (repo/"app.py").read_text() == "import os\nvalue = 2\nmore = 3\n" and
  (repo/"util.py").read_text() == "helper = 2\n". State in the docstring that
  before the R-0317 fix this exact input returned full_fallback because the
  separator became a context line on the first section.

Change — C6, packages/orchestration/diff_repair_apply.py:
  R-0316: the fallback branch returns `files_modified=0` unconditionally and
  the module docstring promises the snapshot restores "every touched file when
  a hunk conflicts". Both are true only while the rollback SUCCEEDS.
  `source_apply._rollback_from_snapshot` catches OSError per entry and appends
  `rollback_incomplete (N file(s)): …` to the errors, leaving those files
  half-restored — and the seam then reports a clean tree.

  Add ONE field to `DiffRepairApplyResult`, last in the field order so existing
  positional construction is unaffected:

    rollback_incomplete: bool = False

  In the FAILED-apply branch only, compute
    rollback_incomplete = any("rollback_incomplete" in e for e in apply_result.errors)
  and return `files_modified=apply_result.files_modified` when it is True,
  `files_modified=0` when it is False. The three early-return paths
  (validation, fence, and the successful apply) keep `rollback_incomplete=False`
  and are otherwise unchanged.

  Correct the module docstring: the snapshot restores every touched file when a
  hunk conflicts AND the restore itself succeeds; when it does not, the
  applicator says so in its errors, `rollback_incomplete` is True and
  `files_modified` carries the real count instead of a reassuring zero. Name
  R-0316. Add the field to the `DiffRepairApplyResult` line of the "Public
  API::" block if that line enumerates fields; otherwise leave the list as is.

  Same commit, ONE test in tests/orchestration/test_diff_repair_apply.py:
  monkeypatch `packages.orchestration.diff_repair_apply.apply_structured_patch`
  with a function returning
    ApplyResult(apply_id="x", success=False, files_modified=1, files_created=0,
                errors=["a.py: diff hunks did not apply cleanly",
                        "rollback_incomplete (1 file(s)): a.py"],
                snapshot_id="s", snapshot_verified=True)
  (import ApplyResult from packages.orchestration.source_apply) and assert the
  seam returns mode full_fallback, applied False, rollback_incomplete True and
  files_modified == 1 — the honest count, not 0. Add one assertion to the
  EXISTING conflicting-hunk test that a real clean fallback has
  rollback_incomplete False and files_modified 0, so both sides are pinned.

Constraints:
  - AGENTS.md in full: self-review loop before every commit, one logical step
    per commit, <500 INSERTIONS per commit, plan.md current before committing,
    clean tree, push after every commit.
  - The change set is EXACTLY these eight paths and nothing else:
    .agent/authored/f111-r15-1.md, .agent/last_block.md, .agent/live_review.md,
    packages/orchestration/diff_repair_response.py,
    packages/orchestration/diff_repair_apply.py,
    tests/orchestration/test_diff_repair_response.py,
    tests/orchestration/test_diff_repair_apply.py, .agent/plan.md,
    .agent/handoff.md. Touching any other path is a scope violation — report it
    instead of doing it.
  - Do NOT modify packages/orchestration/source_apply.py. Both repairs are on
    the F111 side; `_apply_hunks` and `_rollback_from_snapshot` stay as they
    are.
  - Do NOT add a call site for apply_diff_repair. T003 owns the wiring and is
    the NEXT session's first round.
  - Do NOT write any `Done:` paragraph of your own. TEXT-A, TEXT-F and TEXT-G
    are reviewer-authored; apply them verbatim and add nothing
    (planner_reviewer_prompt.md §4.4).
  - If any ordered assertion turns out to contradict the code, do what R14 did:
    implement the production change unweakened, prove the ordered PROPERTY with
    a corrected fixture, write the measurement into the test docstring and
    declare the deviation. Never assert something you measured to be false.
  - Never force-push, never work on main, never merge.

TEXT-A — append verbatim to the END of .agent/live_review.md (commit C3):
Done: R-0313 — a blank context line stripped to "" no longer rejects an
otherwise valid diff. `normalize_diff_blank_context` gives the space back on
the RESPONSE side, where the hunk's declared budget still distinguishes body
from tail, and `diff_repair_response_to_patch` splits the normalised text.
`_apply_hunks` is unchanged, so the trailing-"" trap that would have made the
last hunk over-consume is structurally out of reach: the walk uses
`splitlines()`, which never produces the phantom. Verified at the R14 gate by
value, in both directions: `_apply_hunks('a\n\nb\n', diff)` returns None on the
raw stripped diff and 'a\n\nB\n' on the normalised one, and the normaliser is
byte-identity on a diff that needs no repair. Resolved — with the separator
defect it introduced registered separately as R-0317.

TEXT-F — append verbatim to the END of .agent/live_review.md (commit C3),
after TEXT-A:
- R-0317 (Medium, F111 R14, the blank-context fix eats a file separator):
  `normalize_diff_blank_context` treats a bare "" as a blank context line
  whenever the open hunk still has an old AND a new line left to spend. A model
  that OVER-DECLARES its hunk counts — which this file already records as
  routine, in the D5 note on why the applier does not cross-check headers —
  leaves budget unspent at the end of its body, so the BLANK LINE SEPARATING
  TWO FILE SECTIONS is converted to " " and rides into
  `split_diff_by_path` as a trailing context line of the FIRST file. Measured
  at the R15 gate on the repository's own `DIFF_ONE_FILE` shape
  (`@@ -1,3 +1,3 @@` over a body spending two old and two new lines): the raw
  first section applies to 'import os\nvalue = 1\nmore = 3\n' and returns
  'import os\nvalue = 2\nmore = 3\n', while the normalised section returns
  None. So R14 closed R-0313 and opened a new instance of the same class — a
  valid multi-file answer rejected — for every first file whose hunk is not at
  end of file. Direction is SAFE (rejection, never corruption), and where the
  hunk IS at EOF both forms still apply identically, which is why no test
  caught it. The R14 worker found the contradiction while writing the ordered
  case 3, refused to assert a false property, implemented the production code
  unweakened and declared the deviation — correct on every count. Reviewer-
  caused: the R14 step block specified the budget rule and nothing else. Fix
  direction: a "" is body only when the next NON-BLANK line is also body — not
  a `---`/`+++`/`diff ` header and not end of input — so a separator and a
  trailing artifact both stay untouched. OPEN.

TEXT-G — append verbatim to the END of .agent/live_review.md (commit C3),
after TEXT-F:
### R14 — PASS (2026-08-13)
Reviewed by the main session over 9a17fad2..48c6340e. Every gate was re-run by
the reviewer on this machine; nothing was read off the handback. Transport:
`.remedy-wt/f111r14/BLOCK`, `.agent/authored/f111-r14-1.md` and
`.agent/last_block.md` are byte-identical at 17418 bytes, sha256
1113f75d07f29bd2bb1218a1f793a5917636c0dd55f2d0a3291bc4af8a9ddaaf, and
`.remedy-wt/f111r14/PLAN` matches `.agent/plan.md` at 2008 bytes. Markers:
`^Landed:` 0, `^Done:` 8, `^- R-0` 41, `^### R13 — PASS` 1. Scope: exactly the
eight ordered paths; `source_apply.py` and `diff_repair_apply.py` untouched.

R-0313 proved closed BY VALUE, both directions: `_apply_hunks('a\n\nb\n', …)`
returns None on the raw stripped diff and 'a\n\nB\n' on the normalised one, and
`normalize_diff_blank_context(DIFF_ONE_FILE)` is byte-identical to its input.
Tests re-run by the reviewer: 68 for the three diff-repair files, 55 for the
applier tier — unmoved, as the applier was not touched — and 42 for the
golden-path canary. Per-commit insertions 293/224/70/96/102/104, each under
500. `git status --porcelain` empty, one worktree, `0	0` against the remote.

The declared deviation is UPHELD and is the round's best work. The block
ordered a case-3 test asserting that
`DIFF_ONE_FILE + "\n" + <second section>` normalises to itself. The reviewer
re-measured it: it does not — the separator "" becomes " " — because
`DIFF_ONE_FILE` declares `@@ -1,3 +1,3 @@` over a body that spends only two old
and two new lines, so the hunk still has budget at the separator and the
ordered step-4 rule fires exactly as written. The worker implemented the
production code verbatim and unweakened, proved the ordered PROPERTY with a
first section whose header matches its body, wrote the measurement into that
test's docstring and escalated for a ruling instead of quietly changing either
side. That is the response the split workflow exists to produce.

Registered from it: R-0317. The reviewer measured its real cost — the raw
first section applies to a file that continues past the hunk and returns
'import os\nvalue = 2\nmore = 3\n', while the normalised section returns None —
so R14 closed one instance of "a valid answer rejected" and opened another.
Safe direction, no corruption, and invisible to any test whose first hunk sits
at end of file, which is why it survived a green round. It is the reviewer's
spec defect, not the worker's, and R15 repairs it.

Also noted, not registered: the `#` comment above the fall-through branch in
`diff_repair_response.py` writes `"\\ No newline at end of file"` with a
doubled backslash, where a comment needs one — `source_apply.py` writes it
correctly. The worker reported it and declined to add an unordered seventh
commit that would have broken the mandated C1-C6 item-status shape; that
judgement was right, and R15 carries the fix as an ordered item.

TEXT-D — the COMPLETE new content of .agent/plan.md (commit C7). Replace the
file; do not merge with what is there:
# Plan — F111 Diff-only repair

Branch: feature/f111-diff-only-repair, cut from main at 4e0b762e,
unmerged, no PR by design. Last reviewed SHA: 48c6340e (R14 PASS).
Next free finding ID: R-0318. Open findings: 33 — 42 registered minus
9 resolved. None is High.

## Goal
Repairs stop resending whole files: a repair round carries only the
failure-relevant hunks with a configurable context margin, the model
answers with a schema-enforced unified diff that is fence-checked and
applied strictly, and ANY hunk conflict discards the attempt whole
and falls back to today's full-file round with the reason recorded
(docs/roadmap/features/T2_F111.md).

## Current Step
R15 closes the two reviewer-caused spec defects in T002 so T003 starts
from a clean seam. R-0317: a "" is hunk body only when the next
non-blank line is body too, so a blank line separating two file
sections stops becoming a context line. R-0316: a failed rollback no
longer reports a clean tree — the seam carries `rollback_incomplete`
and stops zeroing `files_modified` when the applicator says restore
failed. T002 is otherwise complete.

## Next Steps
1. R16 — T003: wire `select_repair_hunks`,
   `changed_line_ranges_from_patch` and `apply_diff_repair` into
   `run_builder_bridge_loop`, emit mode and token evidence per repair
   round, add the fixture token comparison. NOTHING imports the three
   T001/T002 modules yet; R16 is the round that makes F111 real.
2. Integration gate, then closure.

## Risks
- The full suite is RED at the merge base with five known ids
  (R-0286): the integration gate compares base against branch.
- Two rounds running, the defect came from the reviewer's authored
  algorithm, not the worker's execution. Any further algorithm spec
  is measured against this repository's own fixtures BEFORE emission,
  not only against a hand-built example.
- All-or-nothing rests entirely on source_apply's durable snapshot;
  `apply_diff_repair` adds no rollback of its own.

Done when — run every command, record the REAL exit code and the REAL counted
value for each. "Green" as a word is a finding.
  a. sha256sum .agent/authored/f111-r15-1.md .agent/last_block.md -> exit 0,
     the two digests identical. (The reviewer runs the cmp against its own
     originals; do not attempt to read `.remedy-wt/`.)
  b. on .agent/live_review.md: grep -c '^Done:' -> 9; grep -c '^- R-0' -> 42;
     grep -c '^### R14 — PASS' -> 1; grep -c '^Landed:' -> prints 0, exit 1.
  c. grep -c '_blank_line_is_hunk_body' packages/orchestration/diff_repair_response.py
     -> 3 (the def, the call, and the docstring or comment mention; report the
     real number and the three line numbers rather than forcing it to 3).
     grep -c 'rollback_incomplete' packages/orchestration/diff_repair_apply.py
     -> report the real number.
  d. VALUE PROBE, the R-0317 regression, run it and paste the real output:
     python3 -c "
     from packages.orchestration.diff_repair_response import normalize_diff_blank_context as n, split_diff_by_path
     from packages.orchestration.source_apply import _apply_hunks
     d='--- a/src/app.py\n+++ b/src/app.py\n@@ -1,3 +1,3 @@\n import os\n-value = 1\n+value = 2\n\n--- a/src/util.py\n+++ b/src/util.py\n@@ -10,2 +10,2 @@\n-helper = 1\n+helper = 2\n'
     print(n(d)==d)
     print(repr(_apply_hunks('import os\nvalue = 1\nmore = 3\n', split_diff_by_path(n(d))['src/app.py'])))"
     -> must print True, then 'import os\nvalue = 2\nmore = 3\n'. Before this
     round it printed False, then None.
  e. VALUE PROBE, R-0313 still closed:
     python3 -c "
     from packages.orchestration.diff_repair_response import normalize_diff_blank_context as n
     from packages.orchestration.source_apply import _apply_hunks
     print(repr(_apply_hunks('a\n\nb\n', n('@@ -1,3 +1,3 @@\n a\n\n-b\n+B\n'))))"
     -> must still print 'a\n\nB\n'.
  f. python3 -m pytest tests/orchestration/test_diff_repair_response.py
     tests/orchestration/test_diff_repair_apply.py
     tests/orchestration/test_diff_repair.py -q -> exit 0. Record the count.
  g. python3 -m pytest tests/orchestration/test_source_apply.py
     tests/orchestration/test_source_apply_transaction.py -q -> exit 0, 55.
     The applier is untouched, so this number must not move.
  h. python3 -m pytest tests/cli/test_golden_path.py -q -> exit 0, canary.
     Record the count.
  i. git status --porcelain -> empty.
     git diff --name-only 48c6340e..HEAD -> exactly the eight paths listed
     under Constraints, no others.
     git show --stat <sha> for EVERY commit -> each insertion count under 500;
     report the numbers.
     git rev-list --left-right --count origin/feature/f111-diff-only-repair...HEAD
     -> 0	0 after the final push.

Handback: completion report + rewrite .agent/handoff.md per AGENTS.md
(feature + round, branch, per-commit table with insertion counts, changed-files
table, the a-i gate results with real exit codes and counted values, open
findings count, item-status table covering C1-C7 exactly once each, next
expected action). This is the SESSION-CLOSING round, so the handoff also
carries a NEXT SESSION block stating: the branch is unmerged with no PR by
design, so Phase 0 must sweep `feature/*` branches to find it; R16/T003 is the
next action and nothing imports the T001/T002 modules until it runs; and that
per docs/agents/planner_reviewer_prompt.md §4.13 the last round of a branch has
no on-disk gate entry by construction, so the next session must NOT open a
repair round to close R15 — its verdict lives in the handoff. Repeat this
Fortschritt line verbatim in the handoff:
Fortschritt: ~74 % (T001 ✅ · T002 ✅ komplett und repariert · T003 offen · R-0313 ✅ · R-0316 ✅ · R-0317 ✅) — Schätzung
──────────────────────────────────────────────────────────────
