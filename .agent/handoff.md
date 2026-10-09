# Handoff — F253 round 26: book round 25, and a poll that would read lost waits for the recorded end (the hardening stage's third repair round)

## Session

SESSION 6 of feature F253 · round 26 · rounds so far 26

Context self-assessment: the reviewer's context holds; the session continues with the repeated audit and the closure sequence.

Fortschritt: ~97 % (S1 to S7, audit, three repair rounds · repeated audit, closure open) — Schätzung

## Range

Review of `eba4b1d65d1a6b0039677caeb0870754810f7f4b`..`e402ab58a1b61fbb98ded37c266b18e5f0415983` (the last commit before this handback, C3).

## Commits

### b6a32b4dd F253 R26 C1: book round 25, resolve R-1210 and R-1207, register R-1216, DECISION F253 D23, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r26.md` | 166/0 | new file, byte copy of `block.md` (166 lines, sha256 `f9101915003426f0a941d3316ca3a507f766102b47f79fba13fcf07f88c237f0`) |
| `.agent/decisions.md` | 10/0 | `append-decisions.txt`'s bytes appended: DECISION F253 D23 |
| `.agent/live_review.md` | 8/0 | `append-live_review.txt`'s bytes appended: round 25's gate entry, R-1210 and R-1207 resolved, R-1216 registered |
| `.agent/plan.md` | 10/12 | `dry-plan.md`, byte for byte |

### dc1cb12a0 F253 R26 C2: an answer that would read lost waits up to two seconds for the recorded end (R-1216, DECISION F253 D23)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/serve_runs.py` | 43/2 | `RECORDED_END_GRACE_SECONDS = 2.0`, `_recorded_end_within`, and the re-read in `order_record_payload` and `run_record_payload` when the state reads `lost` |
| `tests/orchestration/test_serve_runs.py` | 84/0 | the constant's value; a run and an order whose end is written 0.3 seconds later answer `ended`; a run and an order with no end answer `lost` after at least 0.3 seconds |
| `tests/ui_server/test_public_api.py` | 3/1 | existing test: the run POST test, whose answer reads `lost`, sets `RECORDED_END_GRACE_SECONDS` to 0 with `monkeypatch` so that it does not wait; no assertion changed |

### e402ab58a F253 R26 C3: the page says a poll waits up to two seconds for a recorded end (R-1216)

| Path | +/- | Reason |
|---|---|---|
| `docs/system/public-http-api-v1.md` | 8/3 | "Orders" and "Runs": one sentence each on the wait; the generated section is untouched |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's reply, not here (this file is written before the push).
- No pull request opened, no full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull. No command of mine read, listed or wrote the repository's own `.data`. No test started a real provider.

## Verification

0. Preconditions, before any write: `block.md` read whole; every file in `digests.txt` matched its sha256 (Python `hashlib`), `block.md` 166 lines; `git rev-parse HEAD` and `origin/feature/f253-public-http-api` both read `eba4b1d65d1a6b0039677caeb0870754810f7f4b`; `git status --porcelain` empty; `.agent/STOP` absent. `git branch --show-current` read `feature/f253-public-http-api` before each commit.
1. **Gate 1**: `git status --porcelain` empty after C3 (exit 0); C1's byte proofs, run by `.remedy-wt/f253-r26-worker/c1.py` before the commit: live_review post equals pre plus slice True, decisions post equals pre plus slice True, authored copy equals `block.md` True, plan equals `dry-plan.md` True.
2. **Gate 2**: the block's selection from the primary checkout, once: exit 0, `770 passed in 140.22s (0:02:20)`, no FAILED, ERROR or SKIPPED line. Saved at `.remedy-wt/f253-r26-worker/g2.out`.
3. **Gate 3**: `python3 -m ruff check packages/orchestration/serve_runs.py tests/orchestration/test_serve_runs.py tests/ui_server/test_public_api.py` — exit 0, `All checks passed!`.
4. **Gate 4**: `python3 -m apps.cli.main integrity check --json` — exit 0, `"check_count": 6`, all six `pass`, `"fail_count": 0`.
5. **Gate 5**: the open-finding reader — exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1196', 'R-1216']`, as ordered.
6. Gate 6 (after the push): reported in the worker's reply, not here.

While writing: `tests/orchestration/test_serve_runs.py` alone once, `83 passed in 5.65s`, exit 0.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r26.md`: 166 lines, byte-equal, sha256 `f9101915003426f0a941d3316ca3a507f766102b47f79fba13fcf07f88c237f0`.
- `append-live_review.txt` and `append-decisions.txt` each appended to their base blob at `eba4b1d65`: "post equals pre plus slice" True for both.
- `dry-plan.md` to `.agent/plan.md`: byte-equal.

## Deviations & assumptions

- C1's staged diff: the block copy (lines 1 to 172 of the diff) was not read as hunks, as it is proven byte-equal to `block.md`, which I had read; the decisions, live_review and plan hunks were read whole.
- C3: in "Runs" the inserted sentence sits between "printed." and "An unknown job", so the existing lines "An unknown job, or a job with no run, answers 404 / `run_not_found`. The supervisor" were re-wrapped (3 deleted lines in all, none changed in meaning); the block said no other line of the page changes.
- Choices left to me: the helper sleeps `min(0.05, time remaining)` so the last read falls at the grace's end; its poll interval is the private constant `_RECORDED_END_POLL_SECONDS`; the helper's return type is `Any` because it serves both record classes; the ended-test records are written by a daemon thread through `_atomic_write_json` after 0.3 seconds.
- The one existing test changed, `test_a_run_post_starts_the_run_by_the_full_id_and_answers_202_with_its_record` in `tests/ui_server/test_public_api.py`, sets the grace to 0 by `monkeypatch`. Other tests in that file and in `tests/cli/` that read `lost` through a payload without asserting it keep the wait of two seconds each; none was changed.
- The `remedy` command installed on this machine was never run; every Remedy call was `python3 -m apps.cli.main` from the checkout.

## Round verdicts

Round 25's PASS, with R-1210 and R-1207 resolved and R-1216 registered, is booked by C1 above. Round 26's verdict is the reviewer's.

## For the operator, in plain sentences

Round twenty-five's work passed review: a program can now give an order a name, and a resent order with that name is refused while the first one's work is still going. Its test run also showed a rare timing fault: when a program asked about a run in the split second after it finished, Remedy could call it lost although it had ended normally. This round makes Remedy look again for up to two seconds before it calls a run or an order lost. What remains is a repeat of the final check and the closing steps.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and stop.
2. Then the Open PR Gate (rule 2): no pull request for this branch, none to merge.
3. Then book round 26's verdict and resolve what it repaired in the next round's first commit.
4. Then the acceptance audit repeated for the six statements that had gaps.
5. Then the closure sequence per docs/roadmap/STATUS_closure_protocol.md.

Operator questions open: 4.
Open findings: 13 (R-1216, Medium, owned by F253; R-1160, Medium, and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176 and R-1196, Low, owned by F297) — the count names the set before this round's repair is booked.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 25, resolve R-1210 and R-1207, register R-1216, DECISION F253 D23, the plan and the block | done | `b6a32b4dd` |
| C2: the wait for the recorded end (R-1216) | done | `dc1cb12a0` |
| C3: the page states the wait (R-1216) | done | `e402ab58a` |
| Gates 1 to 5 | done | green |
| C4: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
