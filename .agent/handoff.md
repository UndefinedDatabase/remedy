# Handoff — F295 session 1, round 3: book round 2, register R-1140, repair it with four tests

## Session

SESSION 1 of feature F295 · round 3 · rounds so far 3

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~30 % (T001 landed and its test gap repaired, review pending · T002 to T004 open) — Schätzung.

## Range

Review of `a2b102f71`..`4aece9b41`.

## Commits

### 2a7392b52 F295 R3 C1: book round 2, register R-1140, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f295-r3.md` | 104/0 (new) | byte copy of the round 3 block |
| `.agent/live_review.md` | 4/0 | append the F295 R2 gate entry (VERDICT PASS) and register finding R-1140 (Medium) |
| `.agent/plan.md` | 4/6 | rewrite to round 3's current step: book round 2 and repair R-1140 with four tests |

### 4aece9b41 F295 R3 C2: the order file's cost cap and project reach the job, flags win (R-1140)

| Path | +/- | Reason |
|---|---|---|
| `tests/cli/test_do_order_file.py` | 85/0 | four new tests, after the existing contract test: the header's `max-cost-usd` becomes the run job's recorded budget; `--max-cost-usd` wins over the header's value; the header's `project` selects that registered project for the job (the target repository stays unregistered); `--project` wins over a header naming an unknown project |

### F295 R3 C3: handback (self-reference exception — committed by this same write)

| Path | Reason |
|---|---|
| `.agent/handoff.md` | this file, rewritten in full per `AGENTS.md` and `docs/agents/handback_template.md`, as round 3's handback |

## External actions

None. No `gh` command, PR action or worktree operation was needed this round; the branch already
tracked `origin` at the round's base commit and the Open PR Gate was last satisfied in round 2's
predecessor rounds (pull request 310 merged). The push after this C3 commit is reported in the
worker's final reply, not here (write-once rule; this file is written before that push).

## Verification — the four gates, run once each, after C2's commit and before C3's commit

1. `git -C /home/decodeux/Repos/remedy status --porcelain` → empty. Then three silent `cmp` calls
   compared each C1 file against its matching prepared file (`block.md` for the block copy,
   `dry-live_review.md` and `dry-plan.md` otherwise) — all three printed nothing (byte-identical).

2. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r3/run.py /home/decodeux/Repos/remedy 5
   python3 -m ruff check tests/cli/test_do_order_file.py`
   → `exit 0`; `All checks passed!`.

3. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r3/run_selection.py /home/decodeux/Repos/remedy`
   → `exit 0`. No `FAILED` or `ERROR` line, no `process(es) behind` line. Three `SKIPPED` lines
   printed, the same three round 2 read:
   - `tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.`
   - `tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access`
   - `tests/test_repair_context_reviewer_memory.py:257: UI source not found`
   Summary line: `3102 passed, 3 skipped in 43.70s`. (This round's `selection.txt` is narrower than round
   2's — `tests/cli/test_golden_path.py`, `tests/cli/test_do_order_file.py`, `tests/cli/test_do_flags.py`,
   `tests/orchestration/test_order_file.py`, `tests/orchestration/test_live_review_rotation.py` and
   `tests/orchestration/test_integrity_gate.py` — plus every `tests/test_*.py` file at the tree root,
   which is why its count is smaller than round 2's broader selection.)

4. `python3 /home/decodeux/Repos/remedy/.remedy-wt/f295-r3/run.py /home/decodeux/Repos/remedy 3
   python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → `exit 0`; `['R-1138', 'R-1139', 'R-1140']`.

## Authored-text proofs

- `.remedy-wt/f295-r3/block.md` → `.agent/authored/f295-r3.md`: `wc -l` 104/104, sha256
  `88d1a6d3ddcecb6033012a8badf35df9948941284fa7a97196eb5c0eb450e9da`/same, byte comparison equal
  (`cmp` prints nothing).
- `dry-live_review.md` → `.agent/live_review.md` and `dry-plan.md` → `.agent/plan.md`, each copied
  verbatim: both pairs' byte comparison read equal (`cmp` prints nothing).
- Proof: `.agent/live_review.md` equals `git show a2b102f71:.agent/live_review.md` followed by the
  bytes of `append-live_review.txt` — Python equality printed `True`.
- `git diff --cached --numstat` before the C1 commit read exactly the three lines the block named
  (`104 0`, `4 0`, `4 6`, matched by path above under Commits), confirming the base had not moved.
- All four of the block's stated prepared-file sha256 digests were checked with `sha256sum` before
  use: `block.md` `88d1a6d3...e9da`, `dry-live_review.md` `e854097a...9c13`, `dry-plan.md`
  `6c44bb0e...fab0`, `append-live_review.txt` `91c14ef2...974b` — all four matched the block's
  stated values exactly.

## Deviations & assumptions

None against the block's ordered sequence (C1 with its four steps, the four gates, C2, C3) or its
constraints. The new test file section was run standalone while writing it (15 passed, the file's
full count including the 11 pre-existing tests), exactly as the block's constraints section
permits; the four gates above are the one recorded run of everything else. One cosmetic addition
beyond the block's literal four test bodies: a section comment
(`# ── 9a-9d: the header's max-cost-usd and project reach the job, flags win (R-1140) ──`) was
added above the four new tests, matching the file's existing numbered-section convention; this
changes no test behavior and stays inside the block's one named path.

## State

- Branch: `feature/f295-machine-client-contract-v1`, base `a2b102f71` (confirmed equal to
  `origin`'s tip and to `HEAD` before any write).
- Head after C2: `4aece9b41`.
- Head after C3: this handback's own commit, built on `4aece9b41`; a commit cannot state its own
  hash inside its own content, so the exact SHA is left to the worker's final reply.
- Fortschritt: ~30 % (T001 landed and its test gap repaired, review pending · T002 to T004 open) — Schätzung.

## For the operator, in plain sentences

Four more checks now prove that the most money an order file allows really becomes the limit of
the work it starts, and that a value typed on the command line beats the same value written in
the file.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop; nothing here creates
   that file.
2. Otherwise Phase 1 rule 2 — the Open PR Gate.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 3's verdict and the resolution of R-1140 in the next round's first commit.
5. T002: the digest in `remedy status --json`.

Operator questions open: 0.
Open findings: 3 (R-1140 Medium, owned by F295; R-1138 and R-1139 Low, owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 step 1 (block copy + proofs) | done | `wc -l` 104/104, sha256 equal, cmp equal |
| C1 step 2 (dry-* copies) | done | both pairs cmp equal |
| C1 step 3 (byte-equality proof) | done | `True` |
| C1 step 4 (numstat check + self-review) | done | `git diff --cached --numstat` matched the block exactly; diff read clean |
| C1 commit | done | `2a7392b52` |
| C2: header `max-cost-usd` becomes the job's budget | done | test added and green |
| C2: `--max-cost-usd` wins over the header | done | test added and green |
| C2: header `project` selects that registered project | done | test added and green |
| C2: `--project` wins over an unknown header project | done | test added and green |
| C2 commit | done | `4aece9b41` |
| Gate 1 (status + cmp proofs) | done | porcelain empty, all 3 files equal |
| Gate 2 (ruff) | done | `All checks passed!`, exit 0 |
| Gate 3 (selection suite) | done | `3102 passed, 3 skipped`, exit 0 |
| Gate 4 (open finding ids) | done | `['R-1138', 'R-1139', 'R-1140']`, exit 0 |
| C3 handback commit | done | this file |
| Push after C3 | pending | runs immediately after this commit, reported in the worker's final reply |
