# Handback — F025 Pause/resume (global & per node) · Round 9

## Session

SESSION 2 of feature F025 · round 9 · rounds so far 9

The large majority of the session's context budget remained at the point this handback was
written. The round booked round 8's PASS, resolved R-1056's already-landed repair into the ledger
via C2, wrote the Built State to `docs/roadmap/features/T5_F025.md`, ran the checklist
consolidation pass (nothing joined, still 34 items), generated and ran the closure's self-use item
(SU-030, targeting R-1055, through the configured `self_use` role — `claude-cli` /
`claude-sonnet-4-6` — to a `stopped` outcome at `budget_exhausted:max_cost_usd` with its one task
already `staged_review_passed`), and ran this feature's ONE full suite clean (19312 passed, 20
skipped, exit 0). This round closes nothing: the evidence bundle, review package, ledger rotation,
STATUS line and pull request are the closure's second half.

## Range

Review of 1172c5cf3..HEAD

## Commits

### 01c8ee892 F025 R9 C1: copy round 9 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r9-block.md | +167/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r9-built_state.md | +79/-0 | copy of the built_state.md payload |
| .agent/authored/f025-r9-consol_from.txt | +1/-0 | copy of the consol_from.txt payload |
| .agent/authored/f025-r9-consol_to.txt | +8/-0 | copy of the consol_to.txt payload |
| .agent/authored/f025-r9-ledger.md | +4/-0 | copy of the ledger.md payload |
| .agent/authored/f025-r9-plan.md | +30/-0 | copy of the plan.md payload |

289 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 167, plus 122: 79+1+8+4+30 = 122) — matches exactly.

### de19d1a7b F025 R9 C2: book round 8's PASS and resolve R-1056
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | ledger.md appended (bytes to bytes) — the Gate: F025 R8 entry and its Done: R-1056 line |
| .agent/plan.md | +9/-8 | rewritten whole to the plan.md payload — Current Step/Next Steps/Risks moved to round 9 |

4/0, 9/8 — matches the block's stated expectation exactly. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1055']`, the reviewer's own simulated
reading.

### 300d8c2dc F025 R9 C3: write the Built State and consolidate the checklist
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T5_F025.md | +79/-0 | built_state.md appended (bytes to bytes) — the "## Built State (F025, 2026-09-25)" section |
| docs/agents/planner_reviewer_prompt.md | +7/-0 | consol_from.txt's one line replaced by consol_to.txt's eight (append pattern, byte-verified before write) — the fourteenth consolidation paragraph |

79/0, 7/0 — matches the block's stated expectation exactly. `live_checklist_items` over the planner
prompt reads 34 items at both `1172c5cf` and this commit, the same 34 numbers.

### 2c5ccce9e F025 R9 C4: generate and run the closure's self-use item, record its defects
| Path | +/- | Reason |
|---|---|---|
| scripts/self_use_queue.json | +8/-0 | `generate_and_append_if_empty()`'s one write: SU-030 appended, PENDING (`consumed_by` empty) |
| .agent/selfuse_f025/SU-030.md | +7/-0 | the generated job file's own text, copied from the run's job file path |
| .agent/selfuse_f025/entry_and_job_file.txt | +5/-0 | entry id/title/provenance/consumed_by + job file path |
| .agent/selfuse_f025/execution_config.txt | +39/-0 | the run's `ExecutionConfig`, JSON, sorted keys |
| .agent/selfuse_f025/result_state.txt | +9/-0 | job/task state, stop reason/source/request id, errors |
| .agent/selfuse_f025/timing.txt | +3/-0 | started/finished/job-created timestamps |
| .agent/selfuse_f025/full_transcript.txt | +14/-0 | job id/title/state, stop fields, execution config, per-task summary |
| .agent/selfuse_f025/run_defects.txt | +3/-0 | every string `describe_self_use_run_defects` returned for the run's own `JobPlan` |

88 insertions total, under the cap. `python3 -m pytest tests/docs/ -q -p no:cacheprovider` read
`327 passed` at exit 0 immediately before this commit.

### (pending) F025 R9 C5: record the closure suite transcript and rewrite handoff for round 9
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-closure-suite.txt | measured below | the full suite's command, real exit code, wall time, summary line and bad-node-id list (NONE) |
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- `bash -c 'npm --prefix apps/ui run build ...'` — succeeded, `REAL_EXIT=0`, `git status --porcelain`
  stayed empty afterward.
- `mkdir -p /home/decodeux/remedy-gate-scratch` — refused by the sandbox as outside the session's
  working directories; the full-suite log was written under
  `.remedy-wt/f025-r9-worker/gate-scratch/f025-full-suite.txt` instead, per the block's own fallback
  clause (C5(b)), and is reported as a deviation below.
- `python3 -m pytest -n auto -q > .remedy-wt/.../f025-full-suite.txt 2>&1` — the feature's ONE full
  suite run (amend0917-throughput rule 1; constraint 7), `REAL_EXIT=0`, wall time 137s measured /
  136.59s pytest-reported.
- One new job worktree and branch were left behind by the self-use run itself, per constraint 6
  (never created or deleted by this worker directly): `.remedy-wt/job-d0f70d9d45dd4363` /
  `remedy/job-d0f70d9d45dd4363`. `git branch --list 'remedy/job-*'` now counts 46 (was 45 at session
  start). Nothing was deleted; every pre-existing worktree was left alone.
- `git push origin feature/f025-pause-resume` — runs immediately after C5; its real outcome is
  reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 5: nothing is
merged, no evidence job, no zip). No `git stash`, no force-push, no checkout of another branch, no
`npm install`/`npm ci`/`npx`.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f025-pause-resume
$ git log --oneline -1
1172c5cf3 F025 R8 C6: rewrite handoff for round 8
```

```
$ (line count and sha256 of .remedy-wt/f025-r9/block.md, measured)
line_count: 167
sha256: b672ebccfd6c29d3959d251f2b138337440b440bf1c6fd87d463faf91079af09
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees and
several remedy/job-* worktrees already present at session start, PLUS the one new
`.remedy-wt/job-d0f70d9d45dd4363` the self-use run created — left alone, per constraint 6)
$ git branch --list 'remedy/job-*'
46 branches (was 45 at session start; +1 from this round's self-use run, `remedy/job-d0f70d9d45dd4363`)
```

### G1 — payload transport

```
$ (lines/bytes/sha256 of each .remedy-wt/f025-r9/ payload, measured)
built_state.md    79 lines, 6111 bytes, 6bf899e332d7145ad45b969ec59de77ab13db3b6795eae3429239022d2a2438e
consol_from.txt    1 line,    46 bytes, 4aa784fbe92535f6cd688e3dd9e27b7c5aeb5bc9b243dd8923e13a81ade24e04
consol_to.txt      8 lines,  737 bytes, 8cdf3907a663ed01e207fbe10a07171fb548b482b2637e20ae2c9887c707a9da
ledger.md          4 lines, 3855 bytes, 0e62113e0598a1de99c4632858184ce7b4b8abc6f9b88480b0a4a82f8d4c6099
plan.md           30 lines, 1096 bytes, c969f2a7010b67c545a71f4859fa81e9af9bf5a3a35d52512399d54680ec827b
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ python3 -c "committed = git show 01c8ee892:<path>; source = open(<src>, 'rb').read(); committed == source"
f025-r9-block.md        EQUAL
f025-r9-built_state.md  EQUAL
f025-r9-consol_from.txt EQUAL
f025-r9-consol_to.txt   EQUAL
f025-r9-ledger.md       EQUAL
f025-r9-plan.md         EQUAL
```
Each `.agent/authored/f025-r9-*` copy, read back with `git show 01c8ee892:<path>`, is byte-identical
to its `.remedy-wt/f025-r9/` source (block copy included).

### G2 — the records, the Built State and the consolidation

```
$ git diff --numstat -- .agent/live_review.md .agent/plan.md   # C2
4	0	.agent/live_review.md
9	8	.agent/plan.md
```

```
$ python3 -c "committed(de19d1a7b:.agent/live_review.md) == base(1172c5cf3) + ledger.md"
True
$ python3 -c "committed(de19d1a7b:.agent/plan.md) == plan.md"
True
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; print(open_finding_ids(...))"
['R-1008', 'R-1055']
```
Matches the block's stated reviewer reading exactly.

```
$ git diff --numstat -- docs/roadmap/features/T5_F025.md docs/agents/planner_reviewer_prompt.md   # C3
79	0	docs/roadmap/features/T5_F025.md
7	0	docs/agents/planner_reviewer_prompt.md
```

```
$ python3 -c "committed(300d8c2dc:docs/roadmap/features/T5_F025.md) == base(1172c5cf3) + built_state.md"
True
$ python3 -c "live_checklist_items(prompt @ 1172c5cf3) vs live_checklist_items(prompt @ 300d8c2dc)"
base items: 34, C3 items: 34, same numbers: True
```
`consol_from.txt` occurred exactly once in the prompt before the edit; `consol_to.txt` occurred
exactly once after — the containment/append shape the block declared.

### G3 — the linter on this block

```
$ python3 -m apps.cli.main integrity block .remedy-wt/f025-r9/block.md
  [OK] item 1 (size): 167 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): the block states no open-findings count
  [OK] item 24 (gate paths resolve): 0 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): the block orders no gates before a commit
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
REAL_EXIT=0
```

### G4 — the tests and the tree, at C4

```
$ python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/orchestration/test_block_lint.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py
510 passed in 57.68s
REAL_EXIT=0
```

Self-use readings (C4):
- `generate_and_append_if_empty()` appended `SU-030`, "Address ledger finding R-1055", provenance
  `generated (self-use-generator tier 1, ledger scan, R-1055)` — matching the block's stated dry-run
  prediction exactly (R-1008, though lower-numbered and Medium, is skipped by the generator's own
  `_is_repairable` filter: its paragraph's FIX sentence sits beside the standalone word "operator",
  one of `_INELIGIBLE_PATTERNS`).
- `next_self_use_item()` afterward answers the same SU-030, `consumed_by=""` (still pending).
- `run_next_self_use_item(dest_dir=.../f025-r9-selfuse)`: job id `d0f70d9d45dd4363`, title "Address
  ledger finding R-1055". Builder and reviewer: `claude-cli` / `claude-sonnet-4-6` / effort `medium`
  (the configured `self_use` role — never `fake`). State: `stopped`, `stop_reason
  budget_exhausted:max_cost_usd`, `stop_source budget`, `stop_request_id
  budget_4fae00a9df113748`. `run_manifest_error` empty. Task T001: status
  `applied_to_job_workspace`, reviewer_verdict `pass`, final_status `staged_review_passed`, error
  empty — the task itself was reviewed clean before the job's own budget stop; NEVER applied to the
  target checkout (the approval gate the block names).
- `run_defects.txt` verbatim:
  ```
  From describe_self_use_run_defects():

  1. job d0f70d9d45dd4363 (stopped): stop_reason=budget_exhausted:max_cost_usd; stop_source=budget
  ```
- `python3 -m pytest tests/docs/ -q -p no:cacheprovider` (C4(d)): `327 passed` at exit 0.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true}
```
Six `pass`, `fail_count` 0.

```
$ git status --porcelain
(empty, no untracked file)
```

### G5 — the integration gate

```
$ bash -c 'npm --prefix apps/ui run build 2>&1 | tail -2; echo "REAL_EXIT=${PIPESTATUS[0]}"'
✓ built in 2.11s
REAL_EXIT=0
$ git status --porcelain
(empty)
```

```
$ python3 -m pytest -n auto -q   # the ONE full suite, C5(b)
REAL_EXIT=0
Wall time: 137s measured / 136.59s pytest-reported (0:02:16)
Summary line: 19312 passed, 20 skipped, 1 warning in 136.59s (0:02:16)
Bad node ids (failed + errors): NONE
```
`grep -c "^FAILED\|^ERROR"` over the full log: 0. `tests/orchestration/test_import_reachability.py`
and `tests/test_no_orphan_modules.py` hold no bad node (closure precondition 7 clean).

## Authored-text proofs

`.agent/authored/f025-r9-block.md`, `f025-r9-built_state.md`, `f025-r9-consol_from.txt`,
`f025-r9-consol_to.txt`, `f025-r9-ledger.md` and `f025-r9-plan.md` were built with
`shutil.copyfile` from the reviewer's payload files — never retyped, never edited — and G1 compared
every one byte for byte, read back with `git show 01c8ee892:<path>`, against its source: all six
BYTE-IDENTICAL. `.agent/live_review.md` was appended with raw bytes read from `ledger.md`
(`open(...,'rb').read()` concatenation, `write_bytes`); `.agent/plan.md`, `T5_F025.md`'s appendix
and `planner_reviewer_prompt.md`'s replaced span were each written the same byte-exact way. G2's
numstat comparisons confirm every one matches the payloads' expected insertion counts exactly. The
`.agent/selfuse_f025/**` files and `scripts/self_use_queue.json` are the generator's and runner's
own machine-produced output, not reviewer payloads, so no authored-text proof applies to them.

## Deviations & assumptions

1. **Full-suite log path fallback.** `/home/decodeux/remedy-gate-scratch/` is outside the session's
   sandboxed working directories and `mkdir` there was refused; the block's own C5(b) clause names
   this exact fallback ("or under `.remedy-wt/f025-r9-worker/` if the sandbox refuses that path, said
   so"), so the log was written to
   `.remedy-wt/f025-r9-worker/gate-scratch/f025-full-suite.txt` instead. No content or reading is
   affected; only the log's location differs from the block's first-choice path.
2. **The self-use run stopped on budget, not on completion or an approval-gate block.** Its one task
   reached `staged_review_passed` before the job's own `budget_exhausted:max_cost_usd` stop fired —
   recorded verbatim per constraint's "a blocked or stopped job is an outcome to record, not a
   reason to stop." No finding is registered by this worker; `run_defects.txt` carries the one
   string `describe_self_use_run_defects` returned, for the reviewer's next-round registration.
3. **One new job worktree/branch left behind.** `remedy/job-d0f70d9d45dd4363` and its worktree are
   the self-use run's own artifact, per constraint 6 ("the self-use run may leave `remedy/job-*`
   branches, worktrees or evidence directories behind... delete nothing you did not create as
   scratch, never delete a branch"). Reported, not removed.

No payload was edited or retyped. No commit this round touched a path outside the tracked set
constraint 3 names.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 289 insertions, matches the block's expectation (167+122) exactly; all six copies byte-identical |
| C2 | done | 4/0, 9/8 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1055']` |
| C3 | done | 79/0, 7/0 insertions, matches the block's expectation exactly; `live_checklist_items` stays 34 at both ends |
| C4 | done | SU-030 generated (matches the block's dry-run prediction exactly), run to a `stopped` (`budget_exhausted:max_cost_usd`) outcome under the configured `self_use` role, all seven files saved, `tests/docs/` 327 passed |
| C5 | done | full suite 19312 passed / 20 skipped, exit 0, no bad node ids; UI build exit 0; transcript + handoff committed together |
| G1 | done | every payload's lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | ledger/plan/T5_F025/consolidation all equal base-plus-payload; open-finding set and checklist count both matched the block's stated readings |
| G3 | done | 7/7 checkable items pass, exit 0 |
| G4 | done | 510 passed exit 0; self-use readings recorded verbatim; `integrity check` 6/6 pass; tree clean, no untracked file |
| G5 | done | UI build exit 0, full suite exit 0 with no bad node id, closure-precondition-7 files clean |
| G6 | done | reported in the final reply, after C5 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 9. Then the closure's second
half: booking round 9, registering what the self-use run's defects ask for (one candidate against
R-1055's own track, from `run_defects.txt`), any repair the suite requires (none — it read clean),
the evidence bundle and the review package. Then the closing round. Open findings: 2 — `R-1008` and
`R-1055`, both owned by F285 — the count `open_finding_ids` reads at C2. Operator questions open: 4
— the count of `### Q` headings in `.agent/operator_questions.md` at C2.
