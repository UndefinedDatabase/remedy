# Handoff — F290 round 13: the one full suite again, the PR description aligned with F297

## Session

SESSION 6 of feature F290 · round 13 · rounds so far 13

Context self-assessment: comfortable; the round executed its block (C1, A1, C2, the four gates,
C3) in full, found the suite green on the merged tree, and found no deviation from
`.remedy-wt/f290-r13/block.md` (verified sha256
`ed80df3afdf2b5b1502ec3df449cebfc38c20431b86cee9ee43a261f8f8d9a4e`, 100 lines, before starting).
SLOW MODE was active.

## Range

Review of `5aa5ad5c3`..`ec12ac642`. (C3, the commit that writes this handoff together with the PR
body file, is the self-referencing exception the handback template names — a handoff cannot table
the commit that writes it; its path list is given directly below instead of a numstat table.)

## Commits

### 7f48f94c4 F290 R13 C1: book round 12, save the round 13 block and the plan

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f290-r13.md` | 100/0 (new) | byte copy of the round 13 block |
| `.agent/live_review.md` | 2/0 | append the F290 R12 gate entry |
| `.agent/plan.md` | 6/8 | rewrite to round 13's current step |

### ec12ac642 F290 R13 C2: the one full suite again on the merged tree

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f290-closure-suite.txt` | 6/6 | rewritten transcript of the suite run on the merged tree (tree `7f48f94c4`) |

### F290 R13 C3: handback (self-reference exception — committed by this same write)

| Path | Reason |
|---|---|
| `.agent/authored/f290-r13-pr_body.md` | new; PR body template with the suite bullet filled from the round's transcript |
| `.agent/handoff.md` | this file, rewritten per AGENTS.md and the handback template |

## A1 — the UI build

`/home/decodeux/Repos/remedy/apps/ui/node_modules/.bin/vite build`, cwd
`/home/decodeux/Repos/remedy/apps/ui`, via `subprocess.run`. Exit code 0. Last stdout line:
`✓ built in 3.40s`. `git status --porcelain` stayed empty afterward (the build output under
`apps/ui/dist/` is gitignored). Commits nothing, as the block specifies.

## Closure suite

Transcript, quoted whole from `.agent/authored/f290-closure-suite.txt`:

```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 403.48s (measured wrapper); pytest's own reported wall time 402.78s (0:06:42)
summary line: 21311 passed, 22 skipped, 1 warning in 402.78s (0:06:42)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 7f48f94c4 (F290 R13 C1: book round 12, save the round 13 block and the plan)
cost command: python3 scripts/closure_suite_cost.py --feature F290 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1048.65 CPU seconds, 402.79 wall seconds, 21333 tests collected, exit status 0, recorded 2026-10-06T20:33:14Z
This closure's suite used 1048.65 CPU seconds, 6.8 percent more than F200's 981.70, within the 10 percent limit.
```

The suite ran exactly once (`python3 -m pytest -n auto -q`, no marker, no `-k`, no path, no `-x`,
no `--timeout`, `REMEDY_TEST_MAX_WORKERS` unset), timed by a Python wrapper around
`subprocess.run`. The cost script ran exactly once after it. Because the cost exit code was 0
(within the 10 percent limit, not the exit-1 reading finding R-1139 already covers, and not the
exit-2 unreadable-record case), C3's `gh pr edit 310` step proceeded.

## External actions

- `git push origin feature/f290-findings-paydown-v6` after C1 — `5aa5ad5c3..7f48f94c4`.
- `git push origin feature/f290-findings-paydown-v6` after C2 — `7f48f94c4..ec12ac642`.
- `gh pr view 310 --json state,isDraft,baseRefName,headRefName,number` before editing — OPEN, not
  draft, base `main`, head `feature/f290-findings-paydown-v6`.
- `gh pr edit 310 --body-file .agent/authored/f290-r13-pr_body.md` — accepted (suite was green);
  URL printed `https://github.com/UndefinedDatabase/remedy/pull/310`.
- `gh pr view 310 --json body -q .body` — equal to the local file except one trailing newline the
  remote body carries and the local file does not (allowed difference).
- `git push origin feature/f290-findings-paydown-v6` after C3 — reported in the worker's reply,
  not here (write-once rule; this file is written before that push).

## Verification — the four gates, run once each, after C2 and before C3

1. `git status --porcelain` → empty (exit 0). Block copy `cmp .remedy-wt/f290-r13/block.md
   .agent/authored/f290-r13.md` → equal. `.agent/plan.md` `cmp` against
   `.remedy-wt/f290-r13/plan.md` → equal. Ledger proof: `.agent/live_review.md` bytes equal
   `git show 5aa5ad5c3:.agent/live_review.md` followed by
   `.remedy-wt/f290-r13/append-live_review.txt` (134363 bytes total, confirmed by direct byte
   comparison) → equal.

2. The suite of C2: exit code 0; summary line `21311 passed, 22 skipped, 1 warning in 402.78s
   (0:06:42)`; bad node ids NONE — matches the transcript exactly.

3. `python3 -m apps.cli.main integrity check --json` → `{"check_count": 6, ... "fail_count": 0,
   "ok": true, "passed": true, ...}` (exit 0).

4. `python3 -c "import scripts.rotate_live_review as r;
   print(r.open_finding_ids(open('.agent/live_review.md').read()))"` → `['R-1138', 'R-1139']`
   (exit 0).

## Authored-text proofs

- `.remedy-wt/f290-r13/block.md` → `.agent/authored/f290-r13.md`: `wc -l` 100/100, sha256
  `ed80df3afdf2b5b1502ec3df449cebfc38c20431b86cee9ee43a261f8f8d9a4e`/same, byte comparison equal.
- `.remedy-wt/f290-r13/append-live_review.txt` (2123 bytes) appended to `.agent/live_review.md`
  (132240 → 134363 bytes): the resulting file equals `git show 5aa5ad5c3:.agent/live_review.md`
  (132240 bytes) followed by the append slice bytes, confirmed by direct comparison.
- `.remedy-wt/f290-r13/plan.md` → `.agent/plan.md`: byte comparison equal.
- `.remedy-wt/f290-r13/pr_body_template.md` → `.agent/authored/f290-r13-pr_body.md`: `diff` shows
  exactly one changed block, the five-line suite bullet replacing the `<<SUITE_BULLET>>` line,
  with every placeholder (`<SUMMARY LINE>`, `<CODE>`, `<BAD NODES>`, `<LEFTOVERS>`, `<CPU>`) filled
  from the round's own transcript and re-wrapped to keep every line at or under 100 columns (the
  unwrapped substitution would have put two lines over 100; textwrap re-flowed the paragraph with
  the two-space continuation indent, reusing the `- `/`  ` prefixes the template itself used).
  Nothing else in the file differs from the template.

## Deviations & assumptions

None against the block's ordered sequence (C1, A1, C2, the four gates, C3) or its constraints. One
read-only `gh pr view 310 --json mergeable,mergeStateStatus` query was run out of idle curiosity
after C3's `gh pr edit`; it touched no file, made no decision for this round, and its reading
(`mergeable: MERGEABLE`, `mergeStateStatus: UNSTABLE`) is not load-bearing here — the next
session's Phase 1 rule 2 re-reads CI state itself via `gh pr checks 310` before acting on it.
Noting it here only so no out-of-block command goes unrecorded.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if present, write the handoff and stop; nothing here creates
   that file.
2. Otherwise Phase 1 rule 2 — the Open PR Gate merges pull request 310 once hosted CI on its head
   is green (read the run with `gh pr checks 310`; a RUNNING or RED check is work under
   amend0820/amend0929, not a blocker). Round 13's verdict is booked in the next feature's first
   commit. Then Rule A5 claims the next feature.

Open findings: 2 (R-1138 and R-1139, both Low, owned by F297).
Operator questions open: 0.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 bookkeeping commit | done | `7f48f94c4` |
| Push after C1 | done | `5aa5ad5c3..7f48f94c4` origin updated |
| A1 vite build | done | exit 0, `✓ built in 3.40s`, tree stayed clean |
| C2 closure-suite commit | done | `ec12ac642`; suite `21311 passed, 22 skipped`, exit 0; cost exit 0 |
| Push after C2 | done | `7f48f94c4..ec12ac642` |
| Gate 1 (status + byte proofs) | done | all equal |
| Gate 2 (suite reading) | done | exit 0, matches transcript |
| Gate 3 (integrity check) | done | `fail_count` 0 |
| Gate 4 (open findings) | done | `['R-1138', 'R-1139']` |
| C3 PR body file | done | `.agent/authored/f290-r13-pr_body.md`, diff confined to the suite bullet |
| `gh pr edit 310` | done | suite was green; body matches modulo one trailing newline |
| C3 handback commit | done | this file, committed with the PR body file |
| Push after C3 | pending | runs immediately after this commit, reported in the worker's reply |
