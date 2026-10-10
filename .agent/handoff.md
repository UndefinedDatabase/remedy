# Handback — F302 round 8: the closing round

## Session

SESSION 1 of feature F302 · round 8 · rounds so far 8

Context self-assessment: the reviewer's context holds; the session ends here because F302 is
closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F302 is accepted; its pull request waits for the next session's Open PR Gate) —
Schätzung

## Range

Review of `d1f20f924`..`928c5c0de` (two commits on `feature/f302-claude-cli-tokens` — C1
`53a41d473`, C2 `928c5c0de` — plus this handback, C3).

## Commits

### `53a41d473` F302 R8 C1: book round 7, the Built State, save the round 8 block, the STATUS line and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f302-r8.md` | 159/0 | NEW FILE — byte copy of `block.md` |
| `.agent/authored/f302-r8-status_line.txt` | 1/0 | NEW FILE — byte copy of `src/status_line.txt` |
| `.agent/authored/f302-r8-pr_body.md` | 103/0 | NEW FILE — byte copy of `src/pr_body.md` |
| `.agent/live_review.md` | 2/0 | appended `src/ledger-append.txt` — books round 7's PASS verdict |
| `docs/roadmap/features/T3_F302.md` | 20/0 | appended `src/built-state-closure.txt` — the closure's readings |
| `.agent/plan.md` | 6/6 | replaced with `src/plan.md` |

### `928c5c0de` F302 R8 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 0/22 | `scripts/rotate_live_review.py` moved 11 `Gate:` records out |
| `.agent/live_review_archive.md` | 22/0 | `scripts/rotate_live_review.py` moved 11 `Gate:` records in |

### This commit — F302 R8 C3: accept F302 in STATUS with its README sync and the self-use queue

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | 1/1 | copied `sim-STATUS.md` — F302's `[~]` line becomes `src/status_line.txt`'s `[x]` line |
| `README.md` | 13/2 | copied `sim-README.md` — `136 of 304`, Tier 3 row `9 \| 29`, F302's paragraph closes "Accepted in Tier 3 so far:" |
| `scripts/self_use_queue.json` | 1/1 | copied `sim-self_use_queue.json` — `SU-054`'s `consumed_by` becomes `F302` |
| `.agent/handoff.md` | this commit | this file |

(The three content paths' `+/-` cells above were measured by `git diff --numstat` before this
handoff joined the commit, per the block; they are unchanged by the handoff's own addition.)

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f302-claude-cli-tokens` — pending,
  reported in the worker's final reply only (runs after this commit, per the block's `THEN`).
- `gh pr create --repo UndefinedDatabase/remedy ...` — pending, reported in the worker's final
  reply only.
- `gh pr list --repo UndefinedDatabase/remedy --state open ...` — pending, reported in the
  worker's final reply only.
- No `claude` process started. No merge, no branch creation/move/deletion, no force-push, no
  stash entry touched, no worktree added or removed.

## Verification

**Opening block check** (`verify_block.py`): `block.md` sha256
`64d99991c3c2f88daac3fb6fae5fc400774a60aa97e766ec69b90a7669b8f1b8`, line count 159 — both equal
the order's stated values.

**Digest check** (`verify_digests.py`, all 15 entries of `digests.txt`): 15 of 15 comparisons
`True` (`block.md`, `sim-readings.txt`, `src/status_line.txt`, `src/pr_body.md`,
`src/ledger-append.txt`, `src/built-state-closure.txt`, `src/plan.md`, `src/readme-entry.txt`,
`sim-C1-live_review.md`, `sim-T3_F302.md`, `sim-C2-live_review.md`,
`sim-C2-live_review_archive.md`, `sim-STATUS.md`, `sim-README.md`, `sim-self_use_queue.json`).
`ALL_OK: True`.

**Pre-state** (`precheck.py`, before any write): `git rev-parse HEAD` read
`d1f20f924c4827d28b540bb8b35032605efaeae8`, equal to `origin/feature/f302-claude-cli-tokens`'s
tip and to the block's stated base; `git status --porcelain` empty; `git branch --show-current`
read `feature/f302-claude-cli-tokens`; `.agent/STOP` absent.

**C1's byte proofs** (`c1_verify.py`, read-only, run after the one-time `c1_apply.py`):
`.agent/authored/f302-r8.md` == `block.md` `True`; `.agent/authored/f302-r8-status_line.txt` ==
`src/status_line.txt` `True`; `.agent/authored/f302-r8-pr_body.md` == `src/pr_body.md` `True`;
`.agent/plan.md` == `src/plan.md` `True`; `.agent/live_review.md` == `git show
d1f20f924:.agent/live_review.md` + `src/ledger-append.txt` `True`, and also ==
`sim-C1-live_review.md` whole `True`; `docs/roadmap/features/T3_F302.md` == `git show
d1f20f924:docs/roadmap/features/T3_F302.md` + `src/built-state-closure.txt` `True`, and also ==
`sim-T3_F302.md` whole `True`. Block copy reported: line count 159, sha256
`64d99991c3c2f88daac3fb6fae5fc400774a60aa97e766ec69b90a7669b8f1b8`. `git status --porcelain`
before commit showed exactly the six C1 paths; `git diff --stat` and the full diff were read and
matched the intended change with no bug, debug leftover, broken import or unrelated edit. `git
branch --show-current` re-checked immediately before the commit: `feature/f302-claude-cli-tokens`.
Committed as `53a41d473`; `git show --numstat` matched the table above and `sim-readings.txt`'s C1
numstat exactly.

**C2's rotation** (`c2_rotate.py`, ran once): exit 0, whole output:
```
gate records moved: 11
finding pairs moved: 0 (0 records)
resolved-text records moved: 0
old ledger size: 179049 bytes
new ledger size: 153578 bytes
old archive size: 6525108 bytes
new archive size: 6550579 bytes
open findings before: 16
open findings after: 16
written: /home/decodeux/Repos/remedy/.agent/live_review.md and /home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Every line but the `written:` line (which names the primary checkout, not the sim's folder,
because this round ran the real rotation in place) equals `sim-readings.txt`'s rotation output.
`c2_verify.py` (read-only): `.agent/live_review.md` == `sim-C2-live_review.md` `True`;
`.agent/live_review_archive.md` == `sim-C2-live_review_archive.md` `True`. `git status
--porcelain` before commit showed exactly the two ledger files; diff matched `sim-readings.txt`'s
C2 numstat (`0/22` live_review.md, `22/0` live_review_archive.md) exactly. `git branch
--show-current` re-checked before the commit: `feature/f302-claude-cli-tokens`. Committed as
`928c5c0de`; `git show --numstat` matched the table above.

**C3 step 1** (`c3_copy.py`, ran once; `c3_verify1.py` and `c3_verify2.py`, read-only): the three
byte comparisons (`docs/roadmap/STATUS.md` == `sim-STATUS.md`, `README.md` == `sim-README.md`,
`scripts/self_use_queue.json` == `sim-self_use_queue.json`) all `True`. `git diff --numstat`
(unstaged): `13/2 README.md`, `1/1 docs/roadmap/STATUS.md`, `1/1 scripts/self_use_queue.json` —
matches `sim-readings.txt`'s C3 numstat exactly. Content checks: the `status_line.txt` content
occurs exactly once in `docs/roadmap/STATUS.md` and no line of it begins `- [~]`; README contains
`136 of 304`, the Tier 3 row `9 | 29`, and F302's paragraph immediately follows "Accepted in Tier 3
so far:"; `SU-054`'s `"consumed_by"` reads `"F302"`.

**Gate 1** (`gate1.py`): `git status --porcelain` exit 0, showing only the three C3 files modified
(`README.md`, `docs/roadmap/STATUS.md`, `scripts/self_use_queue.json`); all 9 byte comparisons of
every file this round copied or appended, against its prepared file (re-checked, including
`.agent/live_review.md` against its post-rotation form `sim-C2-live_review.md`), `True`.
`ALL_EQUAL: True`.

**Gate 2** (`gate2.py`): `status_line.txt` content occurs exactly once in `docs/roadmap/STATUS.md`
(`count = 1`); no line of `docs/roadmap/STATUS.md` begins `- [~]`. `GATE2 PASS: True`.

**Gate 3** (`gate3.py`, run once):
```
python3 -m pytest -q -rfEs tests/docs/ tests/cli/test_advertised_commands.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/cli/test_golden_path.py tests/test_structure_ratchet.py
```
exit 0, `560 passed in 58.84s` — the block's stated count (`560`) with different seconds (`58.84s`
vs. `60.32s`); no FAILED, ERROR or SKIPPED line.

**Gates 4 and 5** (`gate45.py`, one saved script, two `subprocess.run` calls):
```
python3 -m apps.cli.main integrity check --json
```
exit 0: `{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}` — six checks
`pass`, `fail_count 0`.
```
python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
exit 0: `['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172',
'R-1176', 'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230', 'R-1235']` — matches the block's
ordered list exactly.

**Gate 6**: after the push and the pull request — reported in the worker's final reply only.

## Authored-text proofs

`.agent/authored/f302-r8.md` = `block.md` (sha256 and line count both equal, proven at the
opening check, in C1 and re-proven in Gate 1). `.agent/authored/f302-r8-status_line.txt` =
`src/status_line.txt`, proven byte-equal in C1 and re-proven in Gate 1; its content (without a
trailing newline) occurs exactly once inside `docs/roadmap/STATUS.md` (Gate 2, count 1).
`.agent/authored/f302-r8-pr_body.md` = `src/pr_body.md`, proven byte-equal in C1 and re-proven in
Gate 1 — this is the file passed to `gh pr create --body-file`. The two C1 appends
(`src/ledger-append.txt`, `src/built-state-closure.txt`) each applied by byte append and proven
equal to `git show d1f20f924:<path>` followed by the slice, and the resulting whole files also
proven equal to the reviewer's own simulation (`sim-C1-live_review.md`, `sim-T3_F302.md`);
`.agent/plan.md` applied by a plain file copy of `src/plan.md` and proven byte-equal. C3's three
copies (`docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`) each applied by a
plain file copy of the corresponding `sim-*` file and proven byte-equal.

## Deviations & assumptions

None. C1, C2 and C3's copy/append/rotation steps each ran exactly once, through a one-time script,
with every later proof run by a separate read-only script; `git branch --show-current` was
checked before every commit and read `feature/f302-claude-cli-tokens` each time; the ledger
rotation ran exactly once from the primary checkout; the round's only pytest run was Gate 3's
selection — no `REMEDY_TEST_MAX_WORKERS` set, no `-n` passed, no other test command, no two test
commands run at the same time; no full suite, no mutation, no worktree; no `cd`, no shell call
joined two commands, every copy/hash/run/proof ran as a `cwd`-scoped Python script under
`.remedy-wt/f302-r8-worker/`; no file was written under `/tmp`; no file in `.remedy-wt/f302-r8/`
was modified; no mutation outside the paths each commit named; no stash entry touched, no branch
other than the existing one created, no worktree added or removed; nothing merged, no
force-push, no `git checkout` or `git switch`; no provider call, no `claude` process started;
`.agent/STOP` did not appear at any point; commit subjects carry no leading-slash token and no
absolute path.

This section says nothing about this commit's own self-review, per the block; that is reported in
the worker's final reply only.

## Round verdicts

Rounds 1 to 7 booked in the ledger (round 7 by this round's C1: PASS); round 8's verdict is the
reviewer's, written into the pull request and booked in the next feature's first commit.

## For the operator, in plain sentences

The worker Remedy starts for each step of a job now leaves out the instruction files, skills,
plugins, hooks and tool servers of the operator and the project, and the descriptions of tools its
role never uses. A one-word question now costs about 7,000 tokens before it is answered instead of
21,500 to 28,000, and a small real repair passed its review with the same change both ways while
its first worker call read about 40 percent fewer tokens. Two settings bring each part back, and
both together restore the old start. A new command, `remedy stats calls`, shows how many tokens of
each kind one call reads and writes and what one change that reached its repository cost. One
promised part, a job writing down which start its worker used, moves to the next cleanup feature
because the files that would record it may not grow under the size rule. The maintenance job
Remedy ran on itself before closing used two calls, did what it was asked and was not applied. The
whole test collection passed once on the code that ships. The review package was built and where
it is: `remedy-review-20261010-110542-READY_FOR_REVIEW.zip` in
`/home/decodeux/Repos/remedy-history/zips`. A pull request is open and will be merged at the start
of the next session unless the operator merges it earlier. Sixteen smaller problems stay written
down for the next cleanup feature. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The Open PR Gate, which merges F302's pull request in the NEXT session and never in this one,
   after reading its hosted checks.
3. The booking of round 8's verdict in the next feature's first commit.
4. Rule A5 (the next unchecked line in `docs/roadmap/STATUS.md`).

Operator questions open: 0.
Open findings: 16 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225, R-1230 and R-1235, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 7, the Built State, save the round 8 block, the STATUS line and the PR body | done | 4 of 4 copy proofs + 2 of 2 append proofs `True`; committed `53a41d473` |
| C2: rotate the finding ledger into its archive | done | rotation exit 0; both ledger files byte-equal to the sim; committed `928c5c0de` |
| C3: accept F302 in STATUS with its README sync and the self-use queue | done | three byte-equal copies; content checks all `True`; this commit |
| Gate 1 | passed | status clean to the three C3 files; 9 of 9 byte proofs `True` |
| Gate 2 | passed | STATUS line occurs exactly once; no stray `[~]` line |
| Gate 3 | passed | `560 passed in 58.84s`, exit 0, no FAILED/ERROR/SKIPPED |
| Gate 4 | passed | integrity 6/6 `pass`, `fail_count 0` |
| Gate 5 | passed | open findings list matches exactly |
| Gate 6 | pending | reported in the worker's final reply |
| Push | pending | reported in the worker's final reply |
| Pull request | pending | reported in the worker's final reply |
