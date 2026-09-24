# Handback — F019 Live node materialization · Round 7 (closure sequence, first half)

## Session

SESSION 2 of feature F019 · round 7 · rounds so far 7

This round books round 6's PASS, writes the Built State into
`docs/roadmap/features/T5_F019.md`, runs the checklist consolidation pass
(joins nothing, keeps `docs/agents/planner_reviewer_prompt.md` §3 at 34
items), records the self-use track's answer (NONE), and runs this
feature's ONE full suite, committing its transcript. I had ample context
remaining throughout this round; no session-limit pressure at any point.

## Range

Review of 25d361949..HEAD

## Commits

### 393b43bcc F019 R7 C1: copy round 7 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r7-block.md | +197/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r7-plan.md | +33/-0 | copy of the plan.md payload |
| .agent/authored/f019-r7-product.diff | +99/-0 | copy of the product.diff payload |
| .agent/authored/f019-r7-records.diff | +10/-0 | copy of the records.diff payload |
| .agent/authored/f019-r7-selfuse.py | +16/-0 | copy of the selfuse.py payload |
| .agent/authored/f019-r7-selfuse_result.txt | +6/-0 | copy of the selfuse_result.txt payload |

361 insertions by `git show --numstat` (block's 197 lines + 164); matches
the block's expectation exactly; under the 500-insertion cap.

### 71161a017 F019 R7 C2: book round 6's PASS and advance the plan to the closure
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `Gate: F019 R6 —` entry appended |
| .agent/plan.md | +10/-11 | rewritten to the plan.md payload (round 7 / closure scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions by `git show --numstat`: 2/0 live_review.md, 10/11 plan.md —
matches the block's expectation exactly (2 live_review.md, 10 plan.md).

### b5830f7b5 F019 R7 C3: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | +3/-0 | consolidation paragraph appended to §3 |
| docs/roadmap/features/T5_F019.md | +77/-0 | Built State section appended |

3/0, 77/0 insertions by `git show --numstat`; matches the block's
expectation exactly on every file. `git apply --check` then `git apply`
on product.diff: exit 0 both.

### a3d0fe459 F019 R7 C4: record the closure's self-use track, NONE
| Path | +/- | Reason |
|---|---|---|
| .agent/selfuse_f019/result.txt | +6/-0 | new file, copy of the selfuse_result.txt payload |

6/0 insertions by `git show --numstat`; matches the block's expectation
exactly. `selfuse.py` run from the payload directory in the primary
checkout printed `next_self_use_item()` before: `None`,
`generate_and_append_if_empty()`: `None`, `next_self_use_item()` after:
`None`, `git status --porcelain`: `''` — all four readings equal to the
reviewer's simulated-tree readings, so the copy-and-commit branch applied.

### (this commit) F019 R7 C5: record the closure suite transcript and rewrite handoff for round 7
This file plus `.agent/authored/f019-closure-suite.txt`, one commit —
self-reference exception per the handback template (a handback cannot
table the commit that writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-closure-suite.txt | +6/-0 | full-suite command, real exit code, wall time, summary line, bad node ids (NONE) |
| .agent/handoff.md | rewritten | this handback |

## External actions

- `npm --prefix apps/ui run build` (C5a) — real outcome: `✓ built in
  2.04s`, `REAL_EXIT=0`. `git status --porcelain` immediately after:
  empty.
- `python3 -m pytest -n auto -q` (C5b), output written to
  `/home/decodeux/remedy-gate-scratch/f019-full-suite.txt` — real outcome:
  `REAL_EXIT=0`, wall time 186 s (externally timed) / 185.67 s (pytest's
  own report), summary `19092 passed, 20 skipped, 1 warning in 185.67s
  (0:03:05)`, no bad node ids.
- `git push origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`, no worktree add/remove
  (constraint 6 leaves every existing worktree alone; C5's gate needed
  none).

## Verification

G1 TRANSPORT — all 5 payloads measured against the block's PAYLOADS
table, all matched (line count, byte count, sha256):
```
records.diff          lines=10 bytes=6914 sha256=aa4cd42d8289524c949ab20dee49d4e5ad5665a697a397007cc54413c7d056ff
plan.md                lines=33 bytes=1254 sha256=539b3642aa431dd86d06318a7cb932fb7bc10623bc2149f050c61e147123d977
product.diff            lines=99 bytes=7620 sha256=70cbdd5884c1be9d939e5d612a104e947206a3d5d9e785f78469d88c7ac58659
selfuse_result.txt      lines=6  bytes=274  sha256=2a7fbd73f2149ad7b2e281fccff3074d90dde1ccc05543a7fe69f5e8870fd0b3
selfuse.py              lines=16 bytes=755  sha256=abcec8f8aa1c9b2add1c379d7a60bd9b935e205587bf55328f38332a64b28245
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r7-*` copy, read back with `git show
393b43bcc:<path>` from C1, matched its source byte for byte (6
comparisons: the block copy against `.remedy-wt/f019-r7/block.md`, plus
the 5 payload copies) — `ALL_TRANSPORT_OK: True`.

G2 THE RECORDS, THE BUILT STATE AND THE CONSOLIDATION — at C2
(`71161a017`), `.agent/live_review.md` read 320139 bytes, sha256
`9295b21a494ad1c58789d872393ed55771dd6bedfb14a84023740fa00583e858`
(MATCH); `.agent/plan.md` read 1254 bytes, sha256
`539b3642aa431dd86d06318a7cb932fb7bc10623bc2149f050c61e147123d977`
(MATCH, equal to the plan.md payload). At C3 (`b5830f7b5`),
`docs/agents/planner_reviewer_prompt.md` read 100835 bytes, sha256
`49bebeac604c67552aae0d9d5673f1d0cdb1fcd9476b04f2a6bb5b0d69e15eb0`
(MATCH); `docs/roadmap/features/T5_F019.md` read 11306 bytes, sha256
`f27d5401acab218638c7443c7c0f4441046b18a5992c67135a10ed5d0249ae78`
(MATCH). At C4 (`a3d0fe459`), `.agent/selfuse_f019/result.txt` read 274
bytes, sha256
`2a7fbd73f2149ad7b2e281fccff3074d90dde1ccc05543a7fe69f5e8870fd0b3`
(MATCH, equal to the selfuse_result.txt payload). The count of lines C2
adds to the ledger beginning `Gate: F019 R6 — ` is 1 (measured over C2's
diff of `.agent/live_review.md`). `open_finding_ids`
(`scripts/rotate_live_review.py`) over `.agent/live_review.md`: at
`25d36194` → `['R-0499', 'R-0950', 'R-1008', 'R-1046']`; at C2
(`71161a017`) → the same four — matches the reviewer's reading exactly at
both. `live_checklist_items` (`packages/orchestration/block_lint.py`)
over `docs/agents/planner_reviewer_prompt.md`: at `25d36194` and at C3
(`b5830f7b5`) both read the same 34-item key list `[1..16, 18, 20..31,
33..37]` — unchanged.

G3 THE LINTER ON THIS BLOCK — at C4, in the primary checkout:
```
$ python3 -m apps.cli.main integrity block .remedy-wt/f019-r7/block.md
  [OK] item 1 (size): 197 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 33 lines
  [OK] item 10 (open set recomputed): the block states no open-findings count
  [OK] item 24 (gate paths resolve): 9 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G4 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```

G4 THE TESTS AND THE TREE — real transcript, primary checkout, at C4:
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py 2>&1 | tail -3; echo "REAL_EXIT=${PIPESTATUS[0]}"'
........................................................................ [ 94%]
...............................                                          [100%]
534 passed, 1 skipped in 55.88s
REAL_EXIT=0
```
Matches the reviewer's simulated-tree reading of `534 passed, 1 skipped`
at exit 0 exactly — the primary checkout's added `.agent/authored/`
block copy did not push any saved-block-parametrized test count higher.
C4's four self-use readings verbatim: `next_self_use_item()` before:
`None`; `generate_and_append_if_empty()`: `None`; `next_self_use_item()`
after: `None`; `git status --porcelain`: `''`.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0. `git status --porcelain`
immediately after: empty, no untracked file.

G5 THE INTEGRATION GATE — UI build's last line `✓ built in 2.04s`, real
exit code 0; `git status --porcelain` after it: empty. The full suite:
real exit code 0, wall time 186 s / pytest-reported 185.67s (0:03:05),
summary line `19092 passed, 20 skipped, 1 warning in 185.67s (0:03:05)`,
bad node ids: NONE. All written to
`.agent/authored/f019-closure-suite.txt`. Neither
`tests/orchestration/test_import_reachability.py` nor
`tests/test_no_orphan_modules.py` holds a bad node — the full-suite run
exited 0 with no failed or errored node anywhere, so neither file is
among them (closure precondition 7 satisfied).

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f019-r7-*` (the block copy
plus the 5 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from C1 (`393b43bcc`) with `git show
393b43bcc:<path>` and compared byte for byte against its source: all 6
`BYTE-IDENTICAL` (G1 above). `records.diff` was applied with `git apply`
after `git apply --check` passed (exit 0 both), never retyped or edited;
its resulting file contents (`.agent/live_review.md`) were verified by
byte count and sha256 against the reviewer's own reading at C2 (G2
above) — `MATCH`; `.agent/plan.md` was separately rewritten whole via
`shutil.copyfile` from its payload and also confirmed `MATCH`.
`product.diff` was applied the same way (`git apply --check` then `git
apply`, both exit 0), never retyped or edited; the two resulting files'
C3 contents were confirmed `MATCH` against the reviewer's reading in G2
above. `selfuse_result.txt` was copied via `shutil.copyfile` into
`.agent/selfuse_f019/result.txt` only after C4's four readings equalled
the reviewer's simulated-tree readings; its C4 content was confirmed
`MATCH` (G2 above). `selfuse.py` was run unedited from the payload
directory as a TOOL and never applied to a tracked file.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1, C2, C3, C4,
then C5), all gates G1–G4 ran before C5 as ordered, G5 (the integration
gate) ran inside C5 as the block requires, and no payload was edited,
retyped or repaired. The round's whole tracked path set matches
constraint 3 exactly: `git diff --name-only 25d361949 HEAD` (measured
through C4) named the six `.agent/authored/f019-r7-*` copies,
`.agent/live_review.md`, `.agent/plan.md`,
`docs/agents/planner_reviewer_prompt.md`,
`docs/roadmap/features/T5_F019.md` and `.agent/selfuse_f019/result.txt`
— this handoff and the closure-suite transcript are added by C5 itself.
Nothing under `packages/`, `apps/`, `tests/` or `scripts/` was touched,
and none of `README.md`, `docs/roadmap/STATUS.md`,
`scripts/self_use_queue.json`, `.agent/decisions.md`,
`.agent/prose_slips.md`, `.agent/candidates.md` or
`.agent/operator_questions.md` was touched. The full suite ran exactly
once, in C5, and nowhere else this round (constraint 7 / amend0917 rule
1). Nothing was merged and nothing was closed: no `gh pr merge`, no `gh
pr create`, no checkout of `main`, no branch deletion, no force-push, no
STATUS edit, no evidence job, no review package.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 361 insertions, matches (197 block + 164) |
| C2 | done | git apply --check and apply both exit 0; 2/10 insertions, matches both files |
| C3 | done | 3/77 insertions, matches; diff applied clean |
| C4 | done | all four self-use readings matched the reviewer's None/None/None/'' exactly; 6 insertions, matches |
| C5 | done | UI build exit 0; full suite exit 0, 19092 passed/20 skipped, transcript committed; handoff rewritten per template |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | all 5 named file digests matched at their commits; 1 new Gate line; open_finding_ids correct at both commits; checklist item list unchanged (34 items) at both commits |
| G3 | done | integrity block: 7/7 checkable items [OK], exit 0 |
| G4 | done | 534 passed, 1 skipped, exit 0 (matches reviewer's sim reading); integrity check all 6 pass, fail_count 0; tree clean |
| G5 | done | UI build exit 0, tree clean after; full suite exit 0, 19092 passed, 20 skipped, no bad node ids; neither closure-precondition-7 file holds a bad node |
| G6 | done | reported in the reply (tree/push/PR state after C5) |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7.
Then the closure's second half — the booking of round 7, any repair the
suite requires, the evidence job and the review package — and then the
closing round. Open findings: 4. Operator questions open: 3.
