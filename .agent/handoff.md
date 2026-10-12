# Handback — F058 round 5: book round 4 (PASS), repair R-1262, the model failover page, and the feature file's Built State

## Session

SESSION 3 of feature F058 · round 5 · rounds so far 5

Context self-assessment: this session read every module it documents in full before writing a
sentence of the page, and checked the page's TOML example by feeding it to `build_failover_chains`,
so the one open risk is that the page's prose about the run's own fallback and about a relaunch rests
on the code of `model_failover.py` and `pingpong_call_record.py` plus the block, not on a fresh run.

Fortschritt: ~85 % (T001 to T003 and the documentation landed · the closure open) — Schätzung

## Range

Review of `786c44bfa`..HEAD.

## Commits

### 7ae04fe4b F058 R5 C1: book round 4 (PASS, R-1262; R-1261 resolved)

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f058-r5.md` | +179/-0 | NEW FILE, copy of the block (179 lines, sha256 `e09f8ae35dad20fd8b6b76f0f22eeb3865a41840e1aba055ac31c34e04f07099`) |
| `.agent/live_review.md` | +6/-0 | round 4's verdict, R-1262, the resolution of R-1261 |
| `.agent/plan.md` | +8/-10 | rewritten for round 5 |

### c3c86f8a3 F058 R5 C2: repair R-1262 (the rate-limit run test's error text)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_model_failover.py` | +18/-7 | the reviewer's prepared file, byte-copied |

### d5e7d4f91 F058 R5 C3: the model failover page and its rows in the docs index

| Path | +/- | Reason |
|---|---|---|
| `docs/system/model-failover-v1.md` | +96/-0 | NEW FILE, the page |
| `docs/README.md` | +2/-0 | quick-find row and system-table row |

### ab67bf9c4 F058 R5 C4: the feature file's Built State

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/features/T3_F058.md` | +31/-0 | `## Built State (F058, 2026-10-12)` appended |

### this commit F058 R5 C5: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | rewritten | this handback; `.agent/plan.md` not touched (its Current Step is still true) |

## External actions

No pull request opened (`gh pr list --state open --json number` read `[]` at the start). No worktree
added or removed. Scratch under `.remedy-wt/f058-r5-worker/` (gate 3 output), gitignored. The push
after this commit is reported in the final reply only.

## Verification

Preconditions: branch `feature/f058-model-failover-chain`; HEAD `786c44bfa2fc...`; status empty; open
PRs `[]`; no `.agent/STOP`. Block 179 lines, sha256 as ordered; `run_selection.py`, `selection.txt` and
the three dry files matched their digests.

1. `git status --porcelain` after C4 → empty. PASS.
2. `python3 -m ruff check tests/orchestration/test_model_failover.py` → `All checks passed!`. PASS.
3. `python3 .remedy-wt/f058-r5/prep/run_selection.py /home/decodeux/Repos/remedy` → exit 0,
   `3426 passed, 3 skipped in 25.01s`. SKIPPED: `tests/test_agent_tooling.py:43` (D12 quarantine,
   F252); `tests/test_install_smoke.py:175` (opt-in, `REMEDY_INSTALL_SMOKE=1`);
   `tests/test_repair_context_reviewer_memory.py:257` ("UI source not found"). No FAILED, ERROR,
   `absent in tree:` or `process(es) behind` line. PASS.
4. `python3 -m apps.cli.main integrity check --json` → `fail_count` 0. PASS.
5. `open_finding_ids` → `['R-1235', 'R-1246', 'R-1251', 'R-1252', 'R-1262']`. PASS.
6. `git log --format=%s 786c44bfa..HEAD` → C4, C3, C2, C1 subjects, newest first. PASS.

The page `docs/system/model-failover-v1.md` is 96 lines and contains no `promot`; its TOML example
parses and passes `build_failover_chains`.

## Authored-text proofs

`cmp` of `dry-live_review.md`, `dry-plan.md` against their paths printed nothing (C1); `cmp` of
`dry-test_model_failover.py` against the test file printed nothing (C2). The block copy reads 179
lines with the digest above.

## Deviations & assumptions

1. The page's TOML example names the second link `provider = "claude"`, `model = "claude-sonnet-4-5"`
   (the providers `create_provider` knows are fake, claude, claude-cli and ollama).
2. The block says "the four structural steps"; the git log shows five structural commits (routing
   keys, provider construction, a call's fields, the run handlers, `parked_session_refs`) and the
   ledger lowered four rows. The Built State therefore says "the structural steps lowered four ledger
   rows" and does not state a step count.
3. Gate 3 ran `3426 passed`, fewer than round 4's 5081, because its selection file differs; the run
   was green and was made once.
4. No mutation proofs, no full suite.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): check first.
2. Phase 1 rule 2, the Open PR Gate: check for open pull requests before starting new work.
3. The next round's first commit books round 5's verdict.
4. The closure's integration gate: the feature's one full suite.

Operator questions open: 0.
Open findings: 5 — R-1235, R-1246, R-1251 and R-1252, owned by F306; R-1262, owned by F058,
repaired this round and awaiting the reviewer's verdict.

## For the operator, in plain sentences

There is now a page that explains backup models: how to set them up, when they are used and when
not, and what the run report says. One check was also made sharper so it really proves that a rate
limit never switches to a backup model.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | 3 paths, numstats as ordered |
| C2 | done | `18 7` |
| C3 | done | page 96 lines, 2 index rows |
| C4 | done | 31 insertions |
| C5 | done | this handback |
| Gate 1 | passed | `git status --porcelain` empty |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | `3426 passed, 3 skipped`, exit 0, no FAILED/ERROR/absent/behind line |
| Gate 4 | passed | `fail_count` 0 |
| Gate 5 | passed | open-id list matched exactly |
| Gate 6 | passed | C1 to C4 subjects, newest first |
| R-1262 | repaired | C2; awaiting the reviewer's verdict |
