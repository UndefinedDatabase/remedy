# Handback — F020 Node lifecycle & glyph language · Round 6

## Session

SESSION 1 of feature F020 · round 6 · rounds so far 6

This round booked round 5's PASS into the live review record, appended the Built State to
`docs/roadmap/features/T5_F020.md` and F020's five design-pack rows to
`docs/ui/design_reference/assumption_log.md`, ran the checklist consolidation pass (34 items,
unchanged, joins nothing), recorded the closure's self-use track answer NONE, and ran this
feature's ONE full test suite in the primary checkout after building the UI. All five commits
landed in the block's ordered sequence; all six gates passed with exact matches to the reviewer's
stated readings; the full suite ran green with no deviations. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 3b4dba98..HEAD

## Commits

### b24d40882 F020 R6 C1: copy round 6 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r6-block.md | +204/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r6-plan.md | +30/-0 | copy of the plan.md payload |
| .agent/authored/f020-r6-product.diff | +102/-0 | copy of the product.diff payload |
| .agent/authored/f020-r6-records.diff | +10/-0 | copy of the records.diff payload |
| .agent/authored/f020-r6-selfuse.py | +16/-0 | copy of the selfuse.py payload |
| .agent/authored/f020-r6-selfuse_result.txt | +6/-0 | copy of the selfuse_result.txt payload |

368 insertions by `git show --numstat` (block's 204 lines + 164); matches the block's expectation
exactly; under the 500-insertion cap.

### 24da87f31 F020 R6 C2: book round 5's PASS and advance the plan to the closure
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | F020 R5 Gate entry appended (records.diff) |
| .agent/plan.md | +8/-10 | rewritten to the plan.md payload |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 2 live_review.md, 8 plan.md — matches the block's expectation exactly; aggregate 10
insertions(+)/10 deletions(-), all deletions attributable to plan.md's rewrite diff.

### 5c6019bd4 F020 R6 C3: write the Built State, log the design-pack assumptions, consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +4/-0 | checklist consolidation paragraph appended (product.diff) |
| docs/roadmap/features/T5_F020.md | +66/-0 | Built State section appended (product.diff) |
| docs/ui/design_reference/assumption_log.md | +5/-0 | F020's five design-pack assumption rows appended (product.diff) |

`git apply --check` on product.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 4 planner_reviewer_prompt.md, 66 T5_F020.md, 5 assumption_log.md — matches the block's
expectation exactly.

### 80f6ecc03 F020 R6 C4: record the closure's self-use track, NONE
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f020/result.txt | +6/-0 | new file: closure precondition 6's self-use track answer, NONE |

`python3 .remedy-wt/f020-r6-payloads/selfuse.py /home/decodeux/Repos/remedy` read `next_self_use_item()
before: None`, `generate_and_append_if_empty(): None`, `next_self_use_item() after: None`,
`git status --porcelain: ''` — all four match the reviewer's stated readings exactly, so
`selfuse_result.txt` was copied whole via `shutil.copyfile` into `.agent/selfuse_f020/result.txt`
and committed. 6 insertions by `git show --numstat` — matches the block's expectation exactly.

### (this commit) F020 R6 C5: record the closure suite transcript and rewrite handoff for round 6
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-closure-suite.txt | new | the full suite's command, real exit code, wall time, summary line and bad node ids (NONE) |
| .agent/handoff.md | rewritten | this handback |

## External actions

- `bash -c 'npm --prefix apps/ui run build ...'` — outcome: success, `✓ built in 2.12s`, exit 0;
  `git status --porcelain` empty immediately after (dist is gitignored).
- `git push origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it. No `gh pr create`, no `gh pr merge` this round: the block forbids both
  (constraint 5).

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f020-node-lifecycle-glyph-language
$ git log --oneline -1
3b4dba983 F020 R5 C5: rewrite handoff for round 5
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r6/block.md
204 lines, sha256=a5a20925d06685dfc18ec135010542c11ac862aa84db4708f3930e16d6d0b01f
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ line count / byte count / sha256 over .remedy-wt/f020-r6-payloads/*
plan.md               lines=30  bytes=1064  sha256=5056d243bff937480c647da8b125378c03fa4fcd28bbd1f63a5d85b5d4a4d56e
product.diff           lines=102 bytes=10674 sha256=cb1532132b5dc9b7964731940cbb5159640f26f90537ff95d8cbce9dab283604
records.diff            lines=10  bytes=7856  sha256=e094805efab1507e85cc3b889143d705bfaab96198ad68ef17b0516193d6fb6c
selfuse.py              lines=16  bytes=755   sha256=abcec8f8aa1c9b2add1c379d7a60bd9b935e205587bf55328f38332a64b28245
selfuse_result.txt      lines=6   bytes=274   sha256=fa857cdf367a76fd2a64b2499fbedf818064defa93c0e24f9fb5ef5dadaf1647
```
All 5 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r6-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r6-block.md                    @ b24d40882: match=True
f020-r6-plan.md                     @ b24d40882: match=True
f020-r6-product.diff                @ b24d40882: match=True
f020-r6-records.diff                @ b24d40882: match=True
f020-r6-selfuse.py                  @ b24d40882: match=True
f020-r6-selfuse_result.txt          @ b24d40882: match=True
```
All 6 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's two files and C3's three files, read with `git show <commit>:<path>`,
   against the block's G2 table)
C2 .agent/live_review.md: bytes=300989 sha256=2a04d2c2efc6abd2101df68227ee99fbe2115600d508c49d405f0688c21c14d4 match=True
C2 .agent/plan.md:        bytes=1064   sha256=5056d243bff937480c647da8b125378c03fa4fcd28bbd1f63a5d85b5d4a4d56e match=True
C3 docs/agents/planner_reviewer_prompt.md:      bytes=101386 sha256=7fc033a724415e46c71f428a25e7bbb5704cabbb171ccaba1c31fe4ab47136d4 match=True
C3 docs/roadmap/features/T5_F020.md:            bytes=10144  sha256=b44e27aa45b623df4fbca62410bffd19cd4e52ca02886d585df14ba3ed5d96c2 match=True
C3 docs/ui/design_reference/assumption_log.md:  bytes=6411   sha256=597c10c1d60ef2fb5ddc50d9088c3a1e9c2919d77f3856edc985c5ac1907478e match=True
C4 .agent/selfuse_f020/result.txt: bytes=274 sha256=fa857cdf367a76fd2a64b2499fbedf818064defa93c0e24f9fb5ef5dadaf1647 match=True
```
All 6 match the block's G2 table exactly.

```
$ git diff 24da87f31^ 24da87f31 -- .agent/live_review.md, counting added lines starting
  "Gate: F020 R5 — "
count = 1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 3b4dba98 and at C2
3b4dba98 open ids: ['R-1008']
24da87f31 (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the reviewer's stated reading exactly (G2).

```
$ live_checklist_items(text) from packages/orchestration/block_lint.py, over
  docs/agents/planner_reviewer_prompt.md at 3b4dba98 and at C3
3b4dba98 keys: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,20,21,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37] (34 items)
5c6019bd4 (C3) keys: same 34 numbers
```
Same 34 numbers at both, matching the reviewer's stated reading exactly (G2).

```
$ python3 -m apps.cli.main integrity block .remedy-wt/f020-r6/block.md
  [OK] item 1 (size): 204 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): the block states no open-findings count
  [OK] item 24 (gate paths resolve): 10 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G4 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```
(G3)

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py
  tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py
  tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
  tests/ui_contracts tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
1412 passed, 5 skipped in 66.51s (0:01:06)
REAL_EXIT=0
```
The reviewer read `1367 passed, 8 skipped` WITHOUT the golden path in its simulated tree; this
tree adds the golden path and the primary checkout's toolchain runs the two eslint nodes of
`tests/ui_contracts/test_ui_lint.py` that skip in a worktree, so the higher pass count and lower
skip count are consistent with the block's stated cause (G4).

```
C4's four readings verbatim:
next_self_use_item() before: None
generate_and_append_if_empty(): None
next_self_use_item() after: None
git status --porcelain: ''
```
All four match the reviewer's stated readings exactly (G4).

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0; `git status --porcelain` empty with no untracked file
immediately after (closure precondition 3) (G4).

```
$ bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 2.12s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

```
$ bash -c 'START=$(date +%s); python3 -m pytest -n auto -q >
  /home/decodeux/remedy-gate-scratch/f020-full-suite.txt 2>&1; REAL_EXIT=$?; END=$(date +%s);
  echo "REAL_EXIT=$REAL_EXIT"; echo "WALL_SECONDS=$((END-START))"'
REAL_EXIT=0
WALL_SECONDS=176
$ tail -5 /home/decodeux/remedy-gate-scratch/f020-full-suite.txt
19111 passed, 20 skipped, 1 warning in 175.07s (0:02:55)
$ grep -c "^FAILED\|^ERROR" /home/decodeux/remedy-gate-scratch/f020-full-suite.txt
0
```
No bad node ids (failed plus errors): NONE. Neither `tests/orchestration/test_import_reachability.py`
nor `tests/test_no_orphan_modules.py` holds a bad node (closure precondition 7). The full command,
real exit code, wall time, summary line and bad-node-id list (NONE) are committed whole at C5 in
`.agent/authored/f020-closure-suite.txt` (G5).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f020-r6-*` (the block copy plus the five payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 6 BYTE-IDENTICAL (G1 above). `records.diff` and `product.diff` were each applied with
`git apply` after `git apply --check` passed (exit 0 both), never retyped or edited; the resulting
files were verified by byte count and sha256 against the block's G2 table — all MATCH.
`.agent/plan.md` was rewritten whole via `shutil.copyfile` from the payload source — never
retyped — and confirmed MATCH against the PAYLOADS table and the G2 table.
`.agent/selfuse_f020/result.txt` was copied whole via `shutil.copyfile` from `selfuse_result.txt`
only after C4's four readings equalled it, and confirmed MATCH against the block's G2 table.
`selfuse.py` was run unmodified from its payload path (never applied, per the block's own
instruction) as a tool, not a text application. The full suite's transcript was written directly
by the pytest redirection at C5 to scratch outside the repository, then its command, exit code,
wall time, summary line and bad node ids were written fresh into
`.agent/authored/f020-closure-suite.txt` — no payload existed for this file to be checked against,
per the block's own design.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1, C2, C3, C4, C5, exactly as ordered. G1
through G4 ran before C5, as the block orders; G5 is the suite C5 itself runs. No payload was
edited, retyped or repaired. The round's tracked path set through C4 matched constraint 3 exactly
(`git diff --name-only 3b4dba98 HEAD` before C5: the six `.agent/authored/f020-r6-*` copies,
`.agent/live_review.md`, `.agent/plan.md`, `.agent/selfuse_f020/result.txt`,
`docs/agents/planner_reviewer_prompt.md`, `docs/roadmap/features/T5_F020.md`,
`docs/ui/design_reference/assumption_log.md` — twelve paths, all named by constraint 3, nothing
under `packages/`, `apps/`, `tests/` or `scripts/`, no edit to any of the seven forbidden paths);
C5 adds exactly the two remaining named paths, `.agent/authored/f020-closure-suite.txt` and
`.agent/handoff.md`. Nothing was merged this round: no `gh pr merge`, no `gh pr create`, no
checkout of `main`, no branch deletion, no force-push, no `git stash` — per constraint 5. The
reviewer's worktrees, the `f015-r*`/`f284-r*`/`f020-r*` worktrees and the `job-*` worktrees/branches
were left untouched — per constraint 6. The full test suite ran exactly once, in C5 — per
constraint 7, and it read green (no red-suite exception needed).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 368 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C2 | done | records.diff apply --check and apply both exit 0; 2/8 insertions, matches; plan advanced |
| C3 | done | 4/66/5 insertions, matches block's expectation exactly |
| C4 | done | all four self-use readings matched the reviewer's; 6 insertions, matches exactly |
| C5 | done | UI build exit 0; full suite ran once, exit 0, 19111 passed/20 skipped; transcript committed |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | all 6 named file digests matched; gate-line count 1; open set R-1008 alone at both; checklist same 34 numbers at both |
| G3 | done | linter real exit 0, all 7 checkable items [OK] |
| G4 | done | 1412 passed, 5 skipped at exit 0 (higher/lower than reviewer's simulated reading for the stated cause); C4 readings matched; integrity check 6/6 pass; tree clean |
| G5 | done | UI build exit 0, tree clean after; full suite exit 0, 176s wall, summary line committed; no bad node ids; neither import-reachability nor orphan-modules test holds a bad node |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 6. Then the closure's
second half — the booking of round 6, any repair the suite requires, the evidence job and the
review package. Then the closing round. Open findings: 1. Operator questions open: 3.
