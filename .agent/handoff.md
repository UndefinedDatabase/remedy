# Handoff — F115 Prompt breakdown & cost report · Round 3

Branch: feature/f115-prompt-cost-report (cut from main at 0d6c97aa). Head after
this round: the C5 commit below. Last REVIEWED SHA: cc635159 (R2 PASS) — every
R3 commit is unreviewed. No PR exists and none was created (per block). R3 was
housekeeping only: no source file and no test file was touched.
Open findings: 3. R-0320 Low (dead `stale_diff_context` stop reason in
`builder_bridge.py`, inherited, deliberately unfixed), R-0321 Low (inventory
miscount — FIXED here, marked `Landed:`, awaiting the reviewer's `Done:`),
R-0322 Medium (suite red inherited from the merge base, deliberately unfixed).
Next free finding ID: R-0323.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1a  | done   | |
| C1b  | done   | |
| C2   | done   | |
| C3   | done   | |
| C4   | done   | |
| C5   | done   | |

## Commits

| SHA | Subject | Insertions |
|-----|---------|-----------|
| d305ee58 | chore(f115): save the R3 step block verbatim | 198 |
| 70ab9a38 | chore(f115): mirror the R3 block into last_block | 149 |
| a7a02560 | chore(f115): register R-0322 for the inherited suite red | 18 |
| 8412f20c | docs(f115): correct the call-site count in the inventory | 3 |
| 43763bf4 | docs(agents): add checklist item 8 on unmeetable gate arithmetic | 17 |
| (C5) | chore(f115): refresh the plan and write the R3 handoff | self-referential; see `git log -1` |

## Changed files

| Path | Commit |
|------|--------|
| .agent/authored/f115-r3-1.md | d305ee58 (new) |
| .agent/last_block.md | 70ab9a38 |
| .agent/live_review.md | a7a02560, 8412f20c |
| .agent/f115_inventory.md | 8412f20c |
| docs/agents/planner_reviewer_prompt.md | 43763bf4 |
| .agent/plan.md | (C5) |
| .agent/handoff.md | (C5) |

## Gates (measured)

- a. `cmp` exit 0. sha256 of both files
  7391dc6c87d624ddc137955782c420c6fe59f62006e4d530e75c8b0f8d0b794e.
  `wc -lc .agent/authored/f115-r3-1.md`: 198 12194.
- b. `^- R-0322`: 1 · `^- R-0`: 3.
- c. `four of the eight` in the inventory: 0 · `four of the seven`: 1 ·
  `^Landed: R-0321` in live_review: 1 · `^Done:`: 0.
- d. `Why this is on disk and not a habit`: 1 (unchanged) ·
  `  8. **Gates whose expected VALUE`: 1 ·
  `git show --numstat 43763bf4 -- docs/agents/planner_reviewer_prompt.md`:
  17 added, 0 deleted · item-8 header among that diff's ADDED lines: 1.
- e. `pytest tests/docs/ -q`: 294 passed in 0.30s, exit 0.
  `pytest tests/cli/test_golden_path.py -q`: 42 passed in 19.73s, exit 0.
  Both unchanged from R2.
- f. `wc -l .agent/plan.md`: 43 (cap 50).
- g. `git status --porcelain` empty. `git diff --name-only 0d6c97aa..HEAD`
  lists exactly 15 paths — the 13 from R1+R2 plus `.agent/authored/f115-r3-1.md`
  and `docs/agents/planner_reviewer_prompt.md`, nothing else.
  `git rev-list --left-right --count origin/feature/…...HEAD`: 0 0.

## Next expected action

T001a is finished: the BUILDER call site is wired through
`compose_builder_prompt` (DECISION F115 D1) and pinned by a behaviour test plus
an `inspect.getsource` wiring guard. The REVIEWER and PLANNER call sites are
still UNWIRED — that is the next work, and R2's gate (j) already did the
reading for the reviewer one: its traced text is `_reviewer_effective_prompt`,
which in structured mode appends the native-schema tail unconditionally, so the
manifest should cover the composed BASE and `segment_manifest_chars <
prompt_chars` records the gap (the F105 D3 precedent). The planner site is
`apps/cli/commands/job.py:236`. After both, T001 proper: persist the manifest,
or a reference to it, alongside the ledger row — additively, with backfill
tolerance, old rows rendering as "unattributed" and never guessed. Then T002
(aggregation + pure renderer + goldens) and T003 (CLI, period comparison, json
schema), then the integration gate, which will meet R-0322's five reds.

Deviations, declared: 93 lines, over the 60-line cap (AGENTS.md DECISION D15).
Cause is mandated content only — the six-row item-status table, the six-row
commit table, the seven-row changed-files table, the seven gate results a-g as
REAL measured values, and the end-of-session resume paragraph the block
explicitly mandates ("the one a cold reader can resume from"). No section was
dropped to meet the cap. No other deviation: TEXT-A…TEXT-E were applied byte for
byte from the authored file itself (`sed`/exact-string replace, never retyped),
and no authored text was adjusted to suit a gate.

Fortschritt: 20 % (R1 ✅ · T001a ✅ · Reviewer-Site · T001 · T002 · T003 offen) — Schätzung
