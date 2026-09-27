# Handoff — F029, round 9

## Session

SESSION 2 of feature F029 · round 9 · rounds so far 9. Context remaining at
handback: ample — the round applied three small diffs, ran the self-use
generator/queue pair, built the UI bundle, took the one full suite
(20118 passed, 20 skipped in 276.36s) and wrote this handoff, all in one
pass with no repair round.

## Range

Review of `caec4b929`..`HEAD` (`HEAD` is this handback's own commit, `F029 R9
C4`, on `feature/f029-subtree-rerun`).

## Commits

### ea0f39296 F029 R9 C1: copy round 9 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r9-block.md | 150/0 | copy of this round's block |
| .agent/authored/f029-r9-closure_docs.diff | 131/0 | copy of the closure_docs.diff payload |
| .agent/authored/f029-r9-plan.md | 32/0 | copy of the plan payload |
| .agent/authored/f029-r9-records.diff | 10/0 | copy of the records.diff payload |

Measured insertions: 323 (block's own line count 150 + 173), matching the
block's expectation exactly, under the 500-line cap.

### 2bd56670a F029 R9 C2: book round 8
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | 2/0 | round 8's Gate entry appended (records.diff) |
| .agent/plan.md | 9/8 | rewrite from the plan payload |

Matches the block's expected numstat (2/0, 9/8) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `records.diff`,
followed by the `plan.md` rewrite. Note: the first write of `.agent/plan.md`
was transcribed with one wrong line ("the ledger rotation, the STATUS line
and the pull request" instead of the payload's "the ledger rotation, the
STATUS line, the README counters and the pull request"); the self-review
diff against the payload caught it before staging or committing, so the
committed content is byte-identical to the payload (sha256
`0300a86994345324b05237ec7093ef138c6468607e945f36243196655948dd8f`,
matching G2's table) — recorded here as a caught-before-commit slip, not a
landed deviation.

### ee1bc2e90 F029 R9 C3: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/agents/planner_reviewer_prompt.md | 8/0 | the checklist consolidation paragraph, appended before "The next consolidation measures against 34." — that line occurs once before and once after (an APPEND, not a replace) |
| docs/roadmap/features/T5_F029.md | 104/0 | the Built State section: T001-T003, acceptance, modules/lists, deliberate absences, findings |

Matches the block's expected numstat (8/0, 104/0) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of
`closure_docs.diff`.

### (pending) F029 R9 C4: record the closure suite transcript and rewrite handoff for round 9
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-closure-suite.txt | new | the full suite's command, real exit code, wall time, summary line, bad node ids (NONE) and the tree SHA (`ee1bc2e90`) |
| .agent/handoff.md | rewrite | this file |

## External actions

`bash -c 'npm --prefix apps/ui run build ...'` — real exit 0, `git status
--porcelain` empty afterward, no files staged from it (the build artifact is
gitignored). `git push origin feature/f029-subtree-rerun` — its real outcome
is reported to the delegator, since C4 cannot contain it. No PR opened, no
merge, no branch checked out or deleted, no force-push, no stash, no
worktree added or removed this round.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty;
  `git branch --show-current` → `feature/f029-subtree-rerun`; `git log
  --oneline -1` → `caec4b929`.
- Block bytes: measured 150 lines, sha256
  `8886ec229b65d8aa439043f856c9b0b3bf8c41c8615e9c967c78b059e8a4a3a3` — both
  match the delegation message's readings exactly.
- `git worktree list | wc -l` → 61. `git branch --list 'remedy/job-*' | wc -l`
  → 50.

**PAYLOADS** — all three matched the table exactly:
`closure_docs.diff` 131 lines / 10385 bytes /
`159ca4e86da72f194b9931823a17e3214a100dd25f992a12a6fb46cd57cec096`;
`plan.md` 32 lines / 1106 bytes /
`0300a86994345324b05237ec7093ef138c6468607e945f36243196655948dd8f`;
`records.diff` 10 lines / 8889 bytes /
`4fc53566efa6f210bf100341827a988ee76e252a349cc483b9eee95c45cfe1a7`.

**G1 TRANSPORT** — each `.agent/authored/f029-r9-*` copy read via `git show
ea0f39296:<path>` equals its source byte for byte (sha256, all four):
block copy `8886ec229b65d8aa439043f856c9b0b3bf8c41c8615e9c967c78b059e8a4a3a3`
== `.remedy-wt/f029-r9/block.md`; closure_docs.diff copy
`159ca4e86da72f194b9931823a17e3214a100dd25f992a12a6fb46cd57cec096` ==
`.remedy-wt/f029-r9-payloads/closure_docs.diff`; plan.md copy
`0300a86994345324b05237ec7093ef138c6468607e945f36243196655948dd8f` ==
`.remedy-wt/f029-r9-payloads/plan.md`; records.diff copy
`4fc53566efa6f210bf100341827a988ee76e252a349cc483b9eee95c45cfe1a7` ==
`.remedy-wt/f029-r9-payloads/records.diff`.

**G2 THE RECORDS** — sha256/bytes of each file read via `git show
<read at>:<path>` equals the reviewer's table exactly:
`.agent/live_review.md` at C2 (`2bd56670a`): 334948 bytes,
`1e863a5ca923efe83dbadbb9169f656f4fc6a782e242ad5b2ac2f7bd9de53e42` — match.
`.agent/plan.md` at C2: 1106 bytes,
`0300a86994345324b05237ec7093ef138c6468607e945f36243196655948dd8f` — match.
`docs/roadmap/features/T5_F029.md` at C3 (`ee1bc2e90`): 13157 bytes,
`81af5df871b7c50d7598fe175ad470c67d485a9ba7d3a52c3a800c44aa9efcd2` — match.
`docs/agents/planner_reviewer_prompt.md` at C3: 107507 bytes,
`3bde8f094e52e7676327639f7c77ee467ce1bf8cdca5a68f03dd9dcef906c1b1` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over
`.agent/live_review.md`'s text at C2 → `[]`, matching the reviewer's stated
reading. `live_checklist_items` (`packages/orchestration/block_lint.py`)
over `docs/agents/planner_reviewer_prompt.md` at `caec4b92` and at C3 both
read the same 34 keys (`[1..16, 18, 20..31, 33..37]`) — no change to the
numbering, confirming the consolidation joined nothing.

**G3 THE LINTER** — `python3 -m apps.cli.main integrity block
.remedy-wt/f029-r9/block.md`, real exit code 0, whole output:
```
  [OK] item 1 (size): 150 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 32 lines
  [OK] item 10 (open set recomputed): states 0; .agent/live_review.md holds 0 open by distinct id, and the block registers 0 and resolves 0, leaving 0
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```

**G4 THE TESTS AND THE TREE** — at C3 (`ee1bc2e90`), serially:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/docs/ tests/orchestration/test_block_lint.py
tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py
tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
→ `596 passed in 60.12s (0:01:00)`, real exit code 0, no `SKIPPED` line (`-rs`
reported none). This differs from the reviewer's simulated-tree reading of
595 passed and 1 skipped exactly as the block predicted: the primary
checkout carries a built `apps/ui` (the C4(b) build and any earlier one),
so the one test the simulated tree skips for a missing `apps/ui/node_modules`
/ dist runs and passes here instead — 596 = 595 + 1, 0 skipped = 1 - 1.
Then `python3 -m apps.cli.main integrity check --json` → six `pass` at
`fail_count: 0` (`handler_import`, `live_review_verdict`,
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`,
`high_blockers_open`), `ok: true`. `git status --porcelain` → empty, no
untracked file (closure precondition 3).

**G5 THE INTEGRATION GATE** —
(a) From a scratch Python file: `generate_and_append_if_empty()` →
`None`; `next_self_use_item()` → `None`. Both match the reviewer's dry-run
reading on the byte-equal C3 tree. `scripts/self_use_queue.json` unchanged
(sha256 `c209340be1e923abbcf91717127436917be59141606f22bd77a4d7e67909a268`
before and after) — nothing written. Closure precondition 6 reads
`self-use NONE (queue exhausted)`.
(b) `bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo
"REAL_EXIT=${PIPESTATUS[0]}"'` → last line `✓ built in 2.21s`, `REAL_EXIT=0`;
`git status --porcelain` after it → empty.
(c) `python3 -m pytest -n auto -q`, log at
`.remedy-wt/f029-r9-worker/full_suite.log` (outside the tracked tree): real
exit code 0, wall time 276.36s (0:04:36) (measured wall-clock 277s), summary
line `20118 passed, 20 skipped, 1 warning in 276.36s (0:04:36)`, bad node ids
(failed + errors): NONE. Written to
`.agent/authored/f029-closure-suite.txt` with the tree SHA `ee1bc2e90` (C3).
`tests/orchestration/test_import_reachability.py` and
`tests/test_no_orphan_modules.py` both hold no bad node in this run
(closure precondition 7).

**Constraint 3** — `git diff --name-only caec4b929`, run once more after
writing this file, lists exactly the block's tracked path set plus
`.agent/handoff.md` itself: `.agent/authored/f029-r9-block.md`,
`.agent/authored/f029-r9-closure_docs.diff`, `.agent/authored/f029-r9-plan.md`,
`.agent/authored/f029-r9-records.diff`, `.agent/live_review.md`,
`.agent/plan.md`, `docs/roadmap/features/T5_F029.md`,
`docs/agents/planner_reviewer_prompt.md`,
`.agent/authored/f029-closure-suite.txt`, `.agent/handoff.md` — 10 paths in
total; `scripts/self_use_queue.json` was NOT touched (G5(a) read `None`
twice); no path outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r9-block.md`, `f029-r9-closure_docs.diff`,
`f029-r9-plan.md` and `f029-r9-records.diff` (C1, `ea0f39296`): each read
back via `git show` equals its source (`.remedy-wt/f029-r9/block.md`,
`.remedy-wt/f029-r9-payloads/closure_docs.diff`,
`.remedy-wt/f029-r9-payloads/plan.md`,
`.remedy-wt/f029-r9-payloads/records.diff`) byte for byte — see G1 above.
`.agent/authored/f029-closure-suite.txt` (C4) is this session's own
measurement transcript, not reviewer-authored text, so it carries no
fidelity comparison; its numbers are the ones measured live in G5(c) above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | copy of block + 3 payloads, 323 insertions matching block's own count + 173 |
| C2 | done | records.diff applied (2/0 live_review.md), plan.md rewritten (9/8) — matches expected numstat |
| C3 | done | closure_docs.diff applied (8/0 planner_reviewer_prompt.md, 104/0 T5_F029.md) — matches expected numstat |
| C4 | done | self-use NONE, UI build green, full suite green, transcript + handoff committed together, pushed |
| G1 transport | done | PASS — all four copies byte-identical by sha256 |
| G2 the records | done | PASS — all four file reads and both function reads match the reviewer's table |
| G3 the linter | done | PASS — real exit 0, all 7 checkable items pass |
| G4 the tests and the tree | done | PASS — 596 passed/0 skipped (explained vs. reviewer's 595/1 by dist presence), exit 0; integrity check 6/6 pass; tree clean |
| G5 the integration gate | done | PASS — self-use both None, UI build exit 0, full suite 20118 passed/20 skipped exit 0, no bad node ids, reachability tests clean |

## Deviations & assumptions

One caught-before-commit slip, not a landed deviation: while rewriting
`.agent/plan.md` in C2, the first write mistyped one line of the payload's
Next Steps item 3 (dropped "the README counters"); the mandatory self-review
diff against the payload caught it before `git add`, and the file was
corrected to be byte-identical to the payload (verified by sha256 and
`diff`) before staging. No other deviation: every gate passed on its first
run; no test went red; no commit was split, reordered or dropped from the
block's ordered C1-C4 sequence; the tracked path set matches constraint 3
exactly with `scripts/self_use_queue.json` untouched.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 9,
then the closure's evidence round — the booking of round 9, any repair the
suite requires, the evidence bundle and the review package — and then the
closing round. Open findings: 0. Operator questions open: 0.
