# Handoff — F287 session 1, round 2: claude-cli carries a validated session reference on every call path (T001 first half, DECISION F287 D2)

## Session

SESSION 1 of feature F287 · round 2 · rounds so far 2

Context self-assessment: the reviewer's context is comfortable; the session continues.

Fortschritt: ~20 % (claim · T001 first half landed, review pending · T001 second half, T002 and T003 open) — Schätzung

## Range

Review of `0dfa2fd36`..HEAD (HEAD is C4 below, the commit that carries this handback).

## Commits

### 82e04b85d F287 R2 C1: book round 1, DECISION F287 D2, the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f287-r2.md` | 150/0 (new) | byte copy of this round's block |
| `.agent/decisions.md` | 10/0 | append DECISION F287 D2, exactly as prepared |
| `.agent/live_review.md` | 2/0 | append the F287 R1 gate entry, exactly as prepared |
| `.agent/plan.md` | 5/5 | rewrite to round 2's current step |

### 86360f0ce F287 R2 C2: claude-cli carries a validated session reference on every call path (T001, DECISION F287 D2)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/pingpong_provider.py` | 45/12 | `build_claude_cli_args` gains a validated `resume_session`; `ClaudeCliProvider` threads `resume` through `_call`, `_call_streamed`, `_call_reviewer_structured`, `_build_impl`, `_review_impl`, `build` and `review`; `supports_resume` unchanged |

### d7145b452 F287 R2 C3: tests for the session reference on every claude-cli call path (T001)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_claude_cli_resume.py` | 183/0 (new) | pins every property DECISION F287 D2 (1) states |

### F287 R2 C4: handback (self-reference exception — the handoff is committed by this same commit)

Measured before the handoff joined it (`git diff --cached --numstat`):

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file, rewritten in full per `docs/agents/handback_template.md` |

## External actions

- `git push -u origin feature/f287-provider-session-continuity` after C4: outcome in the worker's final reply (write-once rule; not known when this file is written).
- No merge, no `git checkout` or `git switch`, no branch moved or deleted, no force-push, no pull, no `gh` command, no pull request.

## Verification

1. Before any write: digests of all four reviewer-prepared files (`block.md`, `append-live_review.txt`, `append-decisions.txt`, `dry-plan.md`), computed by a worker-written Python sha256 script, all matched the prompt's sha256 lines exactly (4/4 MATCH, each len=64). `block.md` read 150 lines (by `splitlines()`), sha256 `5862314a5db7122e11af3a76ed5b1bcde9f77e43d6c47e7d0f031da678663938`. `HEAD` read `0dfa2fd36562e0aa6f8faf632b8d0c09a7174890`, equal to `origin/feature/f287-provider-session-continuity`, and `git status --porcelain` was empty before any write.
2. C1 copy/append step: `.agent/authored/f287-r2.md` read `byte_equal=True` against `block.md`. `.agent/live_review.md`'s append read `byte_equal=True` (base blob + `append-live_review.txt`'s bytes == new file). `.agent/decisions.md` was appended with `append-decisions.txt`'s 2847 bytes, never read whole (streamed sha256 over 1 MiB chunks); its base (2897305 bytes) plus the appended slice hashed to the same sha256 as the file after the append (True). `.agent/plan.md` read `byte_equal=True` against `dry-plan.md`.
3. `git diff --cached --numstat` (before the C1 commit) read exactly the four paths the block names — `150 0` `.agent/authored/f287-r2.md` (new), `10 0` `.agent/decisions.md`, `2 0` `.agent/live_review.md`, `5 5` `.agent/plan.md`. The full cached diff was read before committing (self-review): the plan rewrite, the two appends and the new authored copy all matched the prepared bytes; no unrelated edit found.
4. Gate 1: `git -C /home/decodeux/Repos/remedy status --porcelain` — empty. `git show --numstat --format=` of `86360f0ce` (C2) read exactly `45  12  packages/orchestration/pingpong_provider.py`; of `d7145b452` (C3) read exactly `183  0  tests/orchestration/test_claude_cli_resume.py`.
5. Gate 2: `python3 -m pytest -q -rfEs tests/orchestration/test_claude_cli_resume.py tests/orchestration/test_claude_cli_failure_detail.py tests/orchestration/test_structured_cli_envelope.py tests/orchestration/test_claude_cli_exec_guard.py tests/orchestration/test_session_resume.py tests/orchestration/test_stream_evidence_integration.py tests/cli/test_golden_path.py`, from the primary checkout, run once: exit 0, last line `191 passed in 53.88s`; no `FAILED`, `ERROR` or `SKIPPED` line anywhere in the captured output.
6. Gate 3: `python3 -m ruff check packages/orchestration/pingpong_provider.py tests/orchestration/test_claude_cli_resume.py` — exit 0, `All checks passed!`.
7. Gate 4: `python3 -m apps.cli.main integrity check --json` — exit 0: `{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}`; all six checks (`handler_import`, `live_review_verdict`, `plan_consistency`, `relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`) `pass`.
8. Gate 5 (after the push): reported in the worker's final reply (write-once rule; not known when this file is written).

## Authored-text proofs

- `block.md` → `.agent/authored/f287-r2.md`: 150 / 150 lines, sha256 `5862314a5db7122e11af3a76ed5b1bcde9f77e43d6c47e7d0f031da678663938` / same.
- `append-live_review.txt` → `.agent/live_review.md`: append proof True (base blob + slice, byte for byte).
- `append-decisions.txt` → `.agent/decisions.md`: append proof True (base blob + slice, byte for byte; base never read whole, only its length and a streamed sha256).
- `dry-plan.md` → `.agent/plan.md`: byte-equal, True.

## Deviations & assumptions

None. C1, C2 and C3 landed exactly as the block ordered, each in its own commit, each ending with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; gates 1 to 4 all green; this handback is C4, committed alone, and the push follows it once. Helper scripts under `.remedy-wt/f287-r2-worker/` (gitignored, left untracked) did the digest checks, the copy/append operations, their proofs, and ran the gates; none of them touched any path outside the ones this round's commits name.

## Round verdicts

Round 1 PASS is booked by C1 above (carried in the `append-live_review.txt` slice, re-deriving the F287 R1 gate entry). Round 2's verdict is the reviewer's to give and book in the next round's first commit.

## For the operator, in plain sentences

Remedy's connection to the Claude command-line tool can now hand over the name of an earlier conversation so the tool continues it, and it refuses any name that does not look like a real conversation name, so a damaged record can never smuggle an extra instruction into the command; nothing uses it yet, so Remedy behaves exactly as before; the next step switches it on and makes a refused continuation fall back once to a fresh start.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handoff and stop. (Not present as of this handback.)
2. Phase 1 rule 2 (the Open PR Gate): check for open pull requests before any new branch.
3. Confirm `origin`'s tip equals the tip this handoff names before delegating.
4. Book round 2's verdict in the next round's first commit.
5. Round 3: T001 second half, DECISION F287 D2 (2).

Operator questions open: 1.
Open findings: 8 (R-1160, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157 and R-1158, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 1's verdict, DECISION F287 D2, rewrite the plan | done | `82e04b85d` |
| C2: `build_claude_cli_args` gains validated `resume_session`; `ClaudeCliProvider` threads `resume` | done | `86360f0ce` |
| C3: tests for the session reference on every claude-cli call path | done | `d7145b452` |
| `supports_resume` stays False | done | unchanged, pinned by test |
| Gates 1-4 | done | status clean, numstats exact, 191 passed, ruff clean, integrity 6/6 pass |
| C4 handback commit | done | this file |
| Push, gate 5 | pending | run right after this commit, reported in the worker's final reply |
