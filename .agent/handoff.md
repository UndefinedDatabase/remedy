# Handoff — F253 round 10: book round 9, register R-1195 and R-1196, repair R-1195, remove Q11's records

## Session

SESSION 3 of feature F253 · round 10 · rounds so far 10

Context self-assessment: the reviewer's context is workable after one round; the session continues with S4b.

Fortschritt: ~60 % (S1 to S3, S4a, S6a · S4b, S4c, S5, S6b, S7 open) — Schätzung

## Range

Review of `ef775e2e18372c0920580fed97e691d1c48c7fa7`..HEAD (HEAD is C3 below, which carries this
handback and is the last commit on the branch).

## Commits

### 9ab7b9cba F253 R10 C1: book round 9, register R-1195 and R-1196, the plan and the block

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f253-r10.md` | 155/0 | new file, byte copy of `block.md` |
| `.agent/live_review.md` | 12/0 | `append-live_review.txt`'s bytes appended: round 9's gate entry, the resolutions of R-1192, R-1193 and R-1194, and R-1195 and R-1196 |
| `.agent/plan.md` | 7/6 | `dry-plan.md`, byte for byte |

### d6018af42 F253 R10 C2: a write refuses a path value that holds a slash or a NUL once decoded (R-1195)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/public_api.py` | 7/1 | `answer_public_api_post` answers 400 `api_path_invalid` for a bound value that holds `/` or a NUL, before any command runs |
| `docs/system/public-http-api-v1.md` | 3/2 | the page says so |
| `tests/ui_server/test_public_api.py` | 15/0 | one test sends `/` and a NUL through a stand-in runner and finds no command run |
| `tests/orchestration/test_serve_daemon.py` | 16/0 | one test sends `%00` through a real supervisor, finds 400, the decision open and the refusal ledgered |

### This commit (self-reference)

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file; a handback cannot table the commit that writes it |

## External actions

S0 (the three practice records, DECISION F253 D10). STOP CONDITION MET, nothing deleted. The script
`s0.py` in the worker folder, run with `--list` once, printed:

    MATCH project projects 6762bb1d-c63e-4074-a74c-fed41a6e9154.json file 560 bytes
    MATCH project missions 6762bb1d-c63e-4074-a74c-fed41a6e9154 folder 3356 bytes
    MATCH job jobs 7aceeefff16a489b folder 64776 bytes
    MATCH job job_logs 7aceeefff16a489b folder 695 bytes
    job record contains text: True
    PROBLEMS ['project id matches in a foreign folder']

The project id matches an entry in `missions` (a folder), which is not its own folder (`projects`),
so the block's rule "an id matches in a folder other than its own" holds and nothing was removed. The
mission id `2ecf8a23...` matched no entry name in any of the four folders. `--delete` was not run, so
there is no "after" listing; the folders are as the "before" listing shows. The permission system
refused no call.

- Preconditions, before any write: `git rev-parse HEAD` read `ef775e2e18372c0920580fed97e691d1c48c7fa7`,
  equal to `git rev-parse origin/feature/f253-public-http-api`; `git status --porcelain` was empty;
  `.agent/STOP` was absent; `block.md` read sha256
  `108c7f971f2a423a5ddd5cd129accbcb5e3fa6a62e57f3a66ff1b6c730674dd2` and all seven files listed in
  `digests.txt` matched (Python `hashlib`, 7 of 7 True); `git branch --show-current` read
  `feature/f253-public-http-api` before every commit.
- `git push origin feature/f253-public-http-api`, once, after this commit: reported in the worker's
  reply, not here (this file is written before the push).
- No full suite, no mutation, no worktree, no merge, no new branch, no force-push, no pull, no
  `REMEDY_TEST_MAX_WORKERS`, no `-n`. Outside S0, no command read, listed or wrote the repository's
  `.data`.

## Verification

1. Every commit: its staged diff was written to a file in the worker folder and read whole before the
   commit (C1 209 lines, C2 89 lines; the 155 lines of C1's block copy are proven byte-equal instead).
2. **Gate 1**: `git status --porcelain` empty (exit 0); `.agent/live_review.md` equals its blob at
   `ef775e2e1` followed by `append-live_review.txt`, True; `.agent/authored/f253-r10.md` 155 lines,
   sha256 `108c7f971f2a423a5ddd5cd129accbcb5e3fa6a62e57f3a66ff1b6c730674dd2`; the plan and the four
   files of C2 each byte-equal to its prepared file, all True.
3. **Gate 2**, from the primary checkout, once:

       python3 -m pytest -q -rfEs tests/ui_server/test_public_api.py tests/orchestration/test_serve_daemon.py tests/ui_server/test_command_channel.py tests/test_ble001_ratchet.py tests/orchestration/test_import_reachability.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/docs/ tests/cli/test_golden_path.py

   exit 0, `717 passed in 117.92s (0:01:57)`; no FAILED, ERROR or SKIPPED line.
4. **Gate 3**: `python3 -m ruff check` on the three Python files — exit 0, `All checks passed!`.
5. **Gate 4** (`python3 -m apps.cli.main integrity check --json`): exit 0, `"check_count": 6`, all six
   `pass`, `"fail_count": 0`, `"ok": true`.
6. **Gate 5**: exit 0, `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158',
   'R-1160', 'R-1162', 'R-1172', 'R-1176', 'R-1195', 'R-1196']`.
7. Gate 6 (after the push): reported in the worker's reply, not here.

## Authored-text proofs

- `block.md` to `.agent/authored/f253-r10.md`: 155 lines, byte-equal, sha256
  `108c7f971f2a423a5ddd5cd129accbcb5e3fa6a62e57f3a66ff1b6c730674dd2`.
- `append-live_review.txt` appended to its base blob at `ef775e2e1`: "post equals pre plus slice" True
  (C1 script and gate 1).
- `dry-plan.md` to `.agent/plan.md`, and the four prepared files of C2 to their paths: byte-equal
  (gate 1).

## Deviations & assumptions

S0 deleted nothing, because its stop condition was met (see External actions); the block orders C1
onward in that case and the worker went on. Otherwise None.

## Round verdicts

Round 9's PASS, the resolutions of R-1192, R-1193 and R-1194 and the registration of R-1195 and
R-1196 are booked by C1. R-1195's resolution and round 10's verdict are the reviewer's, written into
the next round's first commit.

## For the operator, in plain sentences

I did not remove the three practice records. The listing showed that the project's number also names
a folder in the missions area, which the instructions treat as a reason to stop and report instead of
deleting, so nothing was deleted and the listing is in this file for the reviewer. Round nine's work
passed review. The review found that the web interface, since it began to decode special characters
in an address, let an address name a file outside Remedy's data folder for one kind of question, and
let one special character make the background service drop the request without an answer or a record.
This round closed both, so such an address is now refused with a clear answer and recorded.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): if it appears, finish the commit in hand, write the handback and
   stop.
2. Then the Open PR Gate (rule 2): there is no pull request for this branch yet, so it finds none to
   merge.
3. Then book round 10's verdict and the resolution of R-1195 in the next round's first commit.
4. Then S4b: decline a result through `remedy job decline`.

Operator questions open: 0.
Open findings: 13 (R-1160 and R-1195, Medium; R-1138, R-1139, R-1143, R-1149, R-1156, R-1157,
R-1158, R-1162, R-1172, R-1176 and R-1196, Low; R-1195 owned by F253 and repaired by C2, awaiting the
reviewer's resolution; the rest owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| S0: remove the three practice records | skipped | stop condition met: the project id also matches an entry in `missions`; nothing deleted |
| C1: book round 9, register R-1195 and R-1196, the plan and the block | done | `9ab7b9cba` |
| C2: refuse a path value holding `/` or a NUL once decoded (R-1195) | done | `d6018af42` |
| Gates 1 to 5 | done | all green, run once each, after C2 and before this file |
| C3: this handback | done | this commit |
| Push, Gate 6 | pending | reported in the worker's reply |
