# Handoff — F300 round 2: book round 1, register and repair R-1232, land T002 and T003

## Session

SESSION 1 of feature F300 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~50 % (claim, T001, T002 and T003 · T004 and closure open) — Schätzung

## Range

Review of `1b54bc1e479564ec19417f05f15966584cb46f8d`..HEAD (seven commits on
`feature/f300-structure-ledger-size-ratchet`: C1, C2, C3, C4 part 1, C4 part 2, C5, and this
handback, C6).

## Commits

### `39fbc928c` F300 R2 C1: save the round 2 block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f300-r2.md` | 183/0 | NEW FILE — byte copy of `block.md`; sha256 `ab44a83c5759b5527f000593cfaeaa144fcc963e700c7638a783af7772dcaeb3`, 183 lines |

### `63ac0704b` F300 R2 C2: book F300 R1 and register R-1232, DECISION F300 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | 10/0 | DECISION F300 D2 appended (`append-decisions.txt`'s bytes) |
| `.agent/live_review.md` | 4/0 | replaced with `dry-live_review.md`: the Gate F300 R1 entry (FAIL) and R-1232 appended |
| `.agent/plan.md` | 13/12 | replaced with `dry-plan.md`: round 2's goal and current step |
| `.agent/prose_slips.md` | 1/0 | appended (`append-prose_slips.txt`'s bytes): the F300 round 1 handback-commit numstat slip |

### `21ee0cd6a` F300 R2 C3: the order, the json entries and the file limit of integrity structure under test (R-1232)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_structure_measure.py` | 55/0 | new class `TestOrderJSONShapeAndFileLimit`: measure order largest-first, the handler's exact `--json` entry dictionaries, the text answer's order, and `--file-limit`'s five invalid values — the four mutations R-1232 names |

### `21bba4faf` F300 R2 C4 (part 1): the structure ledger (T002, DECISION F300 D2)

| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | 2/0 | `structure-ledger-v1.md` registered in both index tables, alphabetically placed |
| `docs/system/structure-ledger-v1.md` | 353/0 | NEW FILE — byte copy of the reviewer-prepared ledger page: the measure, the ratchet, the rule, the boundaries/steps of the 29 largest debts, and the two record tables |

### `9dabf465d` F300 R2 C4 (part 2): the ratchet test (T002, DECISION F300 D2)

| Path | +/- | Reason |
|---|---|---|
| `tests/test_structure_ratchet.py` | 181/0 | NEW FILE — the ratchet: S1–S5 per the block's spec, in the pattern of `tests/test_ble001_ratchet.py` |

Split from the single C4 commit the block describes because the combined diff (ledger + README +
test) measured 536 insertions, over the 500-insertion cap; see Deviations. The block itself
authorizes exactly this split for the test file.

### `088bb7a0e` F300 R2 C5: the structure rule in the self-drive protocol (T003, DECISION F300 D2)

| Path | +/- | Reason |
|---|---|---|
| `docs/agents/self_drive_protocol.md` | 21/0 | "The structure rule" section inserted directly before "What stays with the operator", byte copy of the reviewer-prepared file |

### This commit — F300 R2 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file |

## External actions

None yet. The push is ordered by the block AFTER this commit (the "THEN" section); its outcome is
reported in the worker's final reply, not in this file, because the handback is written and
committed once, before it. No `gh pr create` — the block explicitly orders "Do not open a pull
request." No `gh pr merge`, no new branch beyond the one C0 confirmed, no stash entry touched, no
`git worktree add`/`remove` at any point this round.

## Verification

**Gate 1** (after C0, before C1): a Python script compared every line of `digests.txt` against the
file it names.
```
python3 .remedy-wt/f300-r2-worker/gate1_digests.py
```
Exit 0. All 9 comparisons `True`; `ALL_TRUE: True`.

**Gate 2** (after C5): `git status --porcelain` empty; the C2 byte proofs re-run at this commit;
and `docs/system/structure-ledger-v1.md`, `docs/README.md` and `docs/agents/self_drive_protocol.md`
each equal their prepared file.
```
python3 .remedy-wt/f300-r2-worker/gate2.py
```
Exit 0. All 8 readings `True`: status empty; `decisions.md`/`prose_slips.md` equal base+append;
`live_review.md`/`plan.md` equal their prepared files; the ledger, `docs/README.md` and the
protocol file each equal their prepared file.

**Gate 3**, run once, through a Python wrapper (`subprocess.run`, `cwd=/home/decodeux/Repos/remedy`)
capturing the real exit code:
```
python3 -m pytest -q -rfEs @.remedy-wt/f300-r2/selection.txt
```
Exit **0**. `6697 passed, 3 skipped in 535.95s (0:08:55)`. No FAILED or ERROR line. SKIPPED lines:
`tests/test_agent_tooling.py:43` (D12 quarantine, F252), `tests/test_install_smoke.py:175`
(opt-in, needs network), `tests/test_repair_context_reviewer_memory.py:257` (UI source not found).

**Gate 4**:
```
python3 -m ruff check tests/test_structure_ratchet.py tests/orchestration/test_structure_measure.py
```
Exit **0**. `All checks passed!`

**Gate 5**:
```
python3 -m apps.cli.main integrity check --json
```
Exit **0**. `"check_count": 6`, `"fail_count": 0`, `"ok": true`, `"passed": true`, all six checks
`"status": "pass"` (`handler_import`, `live_review_verdict` — "last Gate verdict FAIL" —
`plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`).
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit **0**. Output, verbatim:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1232']
```
Matches the block's ordered list exactly.

**Non-gate validation runs**, each permitted by the block's own exception ("you may run
`tests/orchestration/test_structure_measure.py` or `tests/test_structure_ratchet.py` alone, one
run at a time, and only after C2"), run sequentially, never concurrently with another test
command: `tests/orchestration/test_structure_measure.py` alone after C3 (31 passed, exit 0);
`tests/test_structure_ratchet.py` alone after C4 (5 passed, exit 0, run twice — once before and
once after the `functools.cache` fix below, both green). `ruff check` over each new/changed test
file was also run once ahead of the official gate 4, immediately after authoring each file; the
first run over `tests/test_structure_ratchet.py` found `UP033` (see Deviations) and was re-run
clean after the fix.

**After the push** (reported in the worker's final reply, not here): `git status --porcelain`
empty, `git stash list`, `git log --oneline -n 7`, and the local tip equal to
`origin/feature/f300-structure-ledger-size-ratchet`.

## Authored-text proofs

`.agent/authored/f300-r2.md` (saved block, C1) equals `block.md` byte for byte: sha256
`ab44a83c5759b5527f000593cfaeaa144fcc963e700c7638a783af7772dcaeb3`, 183 lines, both sides.
`.agent/live_review.md` and `.agent/plan.md` (C2) each equal their prepared `dry-*` file byte for
byte, proved at write time and again read-only at gate 2. `.agent/decisions.md` and
`.agent/prose_slips.md` (C2) each equal their blob at `1b54bc1e4` followed by their append slice's
bytes exactly, proved at write time and again at gate 2. `docs/system/structure-ledger-v1.md`,
`docs/README.md` (C4) and `docs/agents/self_drive_protocol.md` (C5) each equal their prepared file
byte for byte, proved at write time and again read-only at gate 2.
`tests/orchestration/test_structure_measure.py` (C3) and `tests/test_structure_ratchet.py` (C4
part 2) are the worker's own code, not reviewer-authored text; no byte-identity proof applies to
them, only the tests themselves passing and `ruff check` reading clean.

## Deviations & assumptions

- **C4 was split into two commits** — "part 1" (`docs/README.md` and
  `docs/system/structure-ledger-v1.md`, 355 insertions) and "part 2" (`tests/test_structure_ratchet.py`,
  181 insertions) — instead of the single C4 commit the block's prose describes, because the
  combined diff measured 536 insertions, over the 500-insertion cap. The block itself authorizes
  exactly this: "if yours would pass 500, put the test file in (part 2) and say so." The
  reviewer's own dry run of the combined commit measured 454 insertions; this worker's ratchet
  test is longer (181 lines, five tests reading two tables and the live measure) and pushed the
  total over the reviewer's figure.
- **`tests/test_structure_ratchet.py` uses `functools.cache`, not the literal `functools.lru_cache`
  the block's S2 names**, because `ruff check` (gate 4 must read exit 0 on this file) flags
  `functools.lru_cache(maxsize=None)` as `UP033` and rewrites it to `functools.cache` — which is
  `functools.lru_cache(maxsize=None)` under `functools`'s own implementation, so "taken once per
  process" holds identically; only the spelling changed, caught and fixed before the commit that
  introduced the file.
- No other deviation: C0 through C5 and gates 1 through 5 ran exactly as the block ordered, each
  exactly once, in the block's sequence; no file outside each commit's named paths was touched;
  gate 3's pytest selection was the round's only test run against the full selection, with no `-n`
  and no `REMEDY_TEST_MAX_WORKERS`, run once, after C5; no two test commands ran at the same time;
  no mutation, no worktree add/remove, nothing merged; no pull request was opened; `.agent/STOP`
  did not appear at any point.

## Round verdicts

F300 round 1's FAIL, with R-1232 registered, is booked by C2 into `.agent/live_review.md`'s
ledger. Round 2's verdict is the reviewer's.

## For the operator, in plain sentences

Remedy now keeps a written list of its own 162 functions longer than 100 lines and 39 files longer
than 1,000 lines, each with its size, on a page of its documentation. A test fails whenever one of
them grows or a new one appears, and asks for its entry to be lowered when one shrinks, so the
list always tells the truth and the code can only get smaller. For the 29 largest the page says
where each should be cut and in which steps. The rule for paying them down is written into the
protocol the build follows: every fifth feature's clean-up takes one such step, and a feature that
changes a listed function first cuts it where the page says. The reviewer's checks of the first
round found that its tests did not notice when the list's order, its machine-readable answer, or
the check of one of its two limits broke, and this round added tests for exactly those. Nothing
waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Phase 1 rule 2 (the Open PR Gate).
3. Book round 2's verdict in the next round's first commit.
4. T004: R-1160's repair with its red-proof in its own commit, then `run_job`'s safe points in one
   function, its row and the pins lowered.

Operator questions open: 0.
Open findings: 17 (R-1160, Medium, and R-1232, Low, owned by F300; R-1138, R-1139, R-1143, R-1149,
R-1156, R-1157, R-1158, R-1162, R-1172, R-1176, R-1196, R-1219, R-1220, R-1225 and R-1230, Low,
owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C0: base and branch | done | preconditions verified: HEAD `1b54bc1e4`, clean tree, correct branch, no STOP |
| Gate 1 | passed | all 9 digests `True` |
| C1: save the round 2 block | done | sha256/line count equal; committed `39fbc928c` |
| C2: book F300 R1, register R-1232, DECISION F300 D2, the plan | done | all byte proofs `True`; committed `63ac0704b` |
| C3: order, json entries and file limit under test (R-1232) | done | 55 insertions; committed `21ee0cd6a` |
| C4: the structure ledger and its ratchet (T002) | done, deviated | split into part 1 (`21bba4faf`) and part 2 (`9dabf465d`) — declared above |
| C5: the structure rule (T003) | done | 21 insertions; committed `088bb7a0e` |
| Gate 2 | passed | status clean; all 8 byte proofs `True` |
| Gate 3 | passed | 6697 passed, exit 0, no FAILED/ERROR |
| Gate 4 | passed | ruff exit 0, all checks passed |
| Gate 5 | passed | six integrity checks pass, fail_count 0; open findings match the block's list |
| C6: handback | done | this commit |
| Push | pending | reported in the worker's final reply, after this commit |
