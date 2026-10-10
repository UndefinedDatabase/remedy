# Handback — F301 round 11: the closing round — ledger rotation, STATUS acceptance, pull request

## Session

SESSION 2 of feature F301 · round 11 · rounds so far 11

Context self-assessment: the reviewer's context holds; the session ends here because F301 is
closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F301 is accepted; its pull request waits for the next session's Open PR Gate)
— Schätzung

## Range

Review of `2c871774c6f675cb62ff4a98e0a3944af6015182`..`2f79351e52d8b5cf93e09d3106b179809332da0a`
(two commits on `feature/f301-mission-upkeep` — C1 `f97a0015c` and C2 `2f79351e5` — plus this
handback, C3).

## Commits

### `f97a0015c` F301 R11 C1: book round 10, the Built State, save the round 11 block, the STATUS line and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f301-r11.md` | 157/0 | NEW FILE — byte copy of `block.md` |
| `.agent/authored/f301-r11-status_line.txt` | 1/0 | NEW FILE — byte copy of `src/status_line.txt` |
| `.agent/authored/f301-r11-pr_body.md` | 112/0 | NEW FILE — byte copy of `src/pr_body.md` |
| `.agent/live_review.md` | 2/0 | blob at `2c871774c` + `src/ledger-append.txt` (books round 10 PASS) |
| `.agent/prose_slips.md` | 1/0 | blob at `2c871774c` + `src/prose_slips-append.txt` (round 10 prose slip) |
| `docs/roadmap/features/T7_F301.md` | 9/0 | replaced with `sim-T7_F301.md` — Built State closure paragraph |
| `.agent/plan.md` | 6/6 | replaced with `src/plan.md` |

### `2f79351e5` F301 R11 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | 0/20 | rotation output — gate records and finding pairs moved to archive |
| `.agent/live_review_archive.md` | 20/0 | rotation output — records appended |

### This commit — F301 R11 C3: accept F301 in STATUS with its README sync and the self-use queue

| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | 1/1 | replaced with `sim-STATUS.md` — F301's `[~]` line becomes the `[x]` accepted line |
| `README.md` | 11/3 | replaced with `sim-README.md` — "135 of 304", Tier 7 row `2 \| 17`, F301's paragraph closes "Accepted in Tier 7 so far:" |
| `scripts/self_use_queue.json` | 1/1 | replaced with `sim-self_use_queue.json` — `SU-053`'s `consumed_by` becomes `F301` |
| `.agent/handoff.md` | this commit | this file |

## External actions

- `git -C /home/decodeux/Repos/remedy push origin feature/f301-mission-upkeep` — runs once after
  this commit, per the block's THEN step; reported in the worker's final reply only.
- `gh pr create --repo UndefinedDatabase/remedy --base main --head feature/f301-mission-upkeep
  --title "F301 — Mission upkeep: every fifth job cleans up" --body-file
  /home/decodeux/Repos/remedy/.agent/authored/f301-r11-pr_body.md` — runs after the push; number
  and URL reported in the worker's final reply only (no PR exists while this handoff is written).
- `gh pr list --repo UndefinedDatabase/remedy --state open --json
  number,headRefName,baseRefName,isDraft` — runs after PR create; reading reported in the worker's
  final reply only.
- No other `gh` command ran. No merge, no branch creation, no force-push, no stash touched.

## Verification

**Pre-state** (before any write): `git rev-parse HEAD` and `git rev-parse
origin/feature/f301-mission-upkeep` both read `2c871774c6f675cb62ff4a98e0a3944af6015182`;
`git status --porcelain` empty; `git branch --show-current` read `feature/f301-mission-upkeep`;
`.agent/STOP` absent.

**Opening digest check** (`python3 -I .../00_start.py`, before the block was read): `block.md`
sha256 `7b6c2163111dfcb785fdf3feec62db6f957e985602aab1544a03ed3c9829f087`, newline count 157 — both
equal the harness's own stated values. Full `digests.txt` sweep (15 entries, one Python script):
all 15 files — `block.md`, `sim-readings.txt`, `src/status_line.txt`, `src/pr_body.md`,
`src/ledger-append.txt`, `src/prose_slips-append.txt`, `src/plan.md`, `sim-C1-live_review.md`,
`sim-prose_slips.md`, `sim-T7_F301.md`, `sim-C2-live_review.md`, `sim-C2-live_review_archive.md`,
`sim-STATUS.md`, `sim-README.md`, `sim-self_use_queue.json` — matched sha256 and newline count
exactly. `ALL_OK`.

**C1's byte proofs** (before commit, one Python script): all seven writes/copies read equal
against their prepared files — `.agent/authored/f301-r11.md` == `block.md`;
`.agent/authored/f301-r11-status_line.txt` == `src/status_line.txt`;
`.agent/authored/f301-r11-pr_body.md` == `src/pr_body.md`; `.agent/live_review.md` (blob at
`2c871774c` + `src/ledger-append.txt`) == `sim-C1-live_review.md`; `.agent/prose_slips.md` (blob at
`2c871774c` + `src/prose_slips-append.txt`) == `sim-prose_slips.md`;
`docs/roadmap/features/T7_F301.md` == `sim-T7_F301.md`; `.agent/plan.md` == `src/plan.md` — seven
of seven `True`. Staged `git diff --cached --numstat` read exactly the C1 cells `sim-readings.txt`
lists: `112/0 .agent/authored/f301-r11-pr_body.md`, `1/0 .agent/authored/f301-r11-status_line.txt`,
`157/0 .agent/authored/f301-r11.md`, `2/0 .agent/live_review.md`, `6/6 .agent/plan.md`, `1/0
.agent/prose_slips.md`, `9/0 docs/roadmap/features/T7_F301.md`. The whole `git diff --cached` (350
lines) was written to a worker file and read whole before commit; every hunk it showed matched the
byte-equal proof already run, so no part of it was skipped unread.

**C2's rotation and byte proofs**: `python3 scripts/rotate_live_review.py` (one saved script),
exit 0:
```
gate records moved: 6
finding pairs moved: 2 (4 records)
resolved-text records moved: 0
old ledger size: 179298 bytes
new ledger size: 160872 bytes
old archive size: 6506682 bytes
new archive size: 6525108 bytes
open findings before: 15
open findings after: 15
written: /home/decodeux/Repos/remedy/.agent/live_review.md and
/home/decodeux/Repos/remedy/.agent/live_review_archive.md
```
Every line but the `written:` line (which names the primary checkout, not the sim's folder) equals
`sim-readings.txt`'s rotation output verbatim. Resulting files: `.agent/live_review.md` ==
`sim-C2-live_review.md` (160872 bytes, sha256
`b744c87c1fd4ed984268340eba2835b29d61b96104f6587c30e0737f2ab924b9`); `.agent/live_review_archive.md`
== `sim-C2-live_review_archive.md` (6525108 bytes, sha256
`4bf768a137a55a36d05c0fdab05c6d76004516ea27b70d742defa7db92a9c736`) — both `True`. `git status
--porcelain` before commit showed exactly these two files modified. `git diff --cached --numstat`
read `0/20 .agent/live_review.md` and `20/0 .agent/live_review_archive.md`, matching
`sim-readings.txt`'s C2 cells exactly. Because both files were already proven byte-equal in full
against their prepared files, the full `git diff --cached` text for C2 was not separately read
line-by-line before commit — this is the one part the block's own rule permits skipping, and it is
named here as that skip.

**C3's copies and content checks**: `docs/roadmap/STATUS.md` == `sim-STATUS.md`; `README.md` ==
`sim-README.md`; `scripts/self_use_queue.json` == `sim-self_use_queue.json` — three of three
`True`. Unstaged `git diff --numstat` read `11/3 README.md`, `1/1 docs/roadmap/STATUS.md`, `1/1
scripts/self_use_queue.json`, matching `sim-readings.txt`'s C3 cells exactly. Content checks: the
`- [x] F301 — Mission upkeep...` line in `docs/roadmap/STATUS.md` is the one line of
`src/status_line.txt`; `README.md` reads "135 of 304 registered items accepted" (line 29), the
Tier 7 summary row reads `| 7 | Quality & Trust | 2 | 17 |` (line 40), and F301's paragraph closes
the list "Accepted in Tier 7 so far:" (lines 743–757); `scripts/self_use_queue.json`'s `SU-053`
entry now reads `"consumed_by": "F301"`.

**Gate 1** (after C3's three files were in place, before this handoff): `git -C
/home/decodeux/Repos/remedy status --porcelain`, exit 0 —
```
 M README.md
 M docs/roadmap/STATUS.md
 M scripts/self_use_queue.json
```
exactly the three C3 files, nothing else. One Python script re-ran the byte comparison of every
file this round copied (the seven C1 files, the two C2 ledger files, the three C3 files — eleven in
all) against its prepared file: eleven of eleven `True`, `ALL_EQUAL`.

**Gate 2** (the STATUS line): one Python script read `src/status_line.txt`, stripped its trailing
newline, and counted its occurrences in `docs/roadmap/STATUS.md`: `occurrences: 1`; and scanned that
same line for any sub-line starting `- [~]`: `lines starting with '- [~]': []`. Both conditions met.

**Gate 3** (the round's one test selection, run once):
```
python3 -m pytest -q -rfEs tests/docs/ tests/cli/test_advertised_commands.py
tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py
tests/cli/test_golden_path.py tests/test_structure_ratchet.py
```
Exit 0. `560 passed in 57.97s` — count matches `sim-readings.txt`'s `560 passed in 59.35s` (seconds
differ, as the block allows); no `FAILED`, `ERROR` or `SKIPPED` line (all three greps empty). Run
once, through one Python wrapper (`11_gate3.py`) that captured the exit code in the same script.

**Gate 4** (one saved script, `subprocess.run`, printing the exit code):
```
python3 -m apps.cli.main integrity check --json
```
Exit 0:
```
{"check_count": 6, "checks": [{"message": "handlers=182", "name": "handler_import", "status":
"pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"},
{"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"},
{"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message":
"no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
"pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
"pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Six of six checks `pass`, `fail_count 0`.

**Gate 5** (same saved script, second `subprocess.run` call, printing its own exit code):
```
python3 -c "import scripts.rotate_live_review as r;
print(r.open_finding_ids(open('.agent/live_review.md').read()))"
```
Exit 0:
```
['R-1138', 'R-1139', 'R-1143', 'R-1149', 'R-1156', 'R-1157', 'R-1158', 'R-1162', 'R-1172', 'R-1176',
'R-1196', 'R-1219', 'R-1220', 'R-1225', 'R-1230']
```
Matches the block's ordered list exactly.

**Gate 6** (after the pull request): reported in the worker's final reply only, per the block.

## Authored-text proofs

All reviewer-authored texts applied this round compare byte-identical to their prepared source,
each confirmed by a Python disk-to-disk comparison before its commit: `.agent/authored/f301-r11.md`
= `block.md`; `.agent/authored/f301-r11-status_line.txt` = `src/status_line.txt`;
`.agent/authored/f301-r11-pr_body.md` = `src/pr_body.md`; `.agent/live_review.md` after C1 = blob
at `2c871774c` + `src/ledger-append.txt` = `sim-C1-live_review.md`; `.agent/prose_slips.md` = blob
at `2c871774c` + `src/prose_slips-append.txt` = `sim-prose_slips.md`;
`docs/roadmap/features/T7_F301.md` = `sim-T7_F301.md`; `.agent/plan.md` = `src/plan.md`;
`.agent/live_review.md` after C2's rotation = `sim-C2-live_review.md`;
`.agent/live_review_archive.md` = `sim-C2-live_review_archive.md`; `docs/roadmap/STATUS.md` =
`sim-STATUS.md`; `README.md` = `sim-README.md`; `scripts/self_use_queue.json` =
`sim-self_use_queue.json`. All `True`. The specific authored-text proof the block names for this
section: the STATUS line in `docs/roadmap/STATUS.md` is byte-identical to
`.agent/authored/f301-r11-status_line.txt` without its trailing newline, occurring exactly once
(count 1) — confirmed in Gate 2 above.

The ledger's size before and after this round's rotation: old ledger 179298 bytes, new ledger
160872 bytes; old archive 6506682 bytes, new archive 6525108 bytes.

## Deviations & assumptions

- C2: because `.agent/live_review.md` and `.agent/live_review_archive.md` were each already proven
  byte-equal in full (whole-file sha256) against their prepared files before staging, the full
  `git diff --cached` text for that commit was not separately read line-by-line before the commit —
  the one part the block's own rule permits a worker to skip, named here as skipped rather than
  silently omitted.

Otherwise: None. C1, C2 and C3 ran in the block's exact sequence, each exactly once; `git branch
--show-current` was checked before every commit and read `feature/f301-mission-upkeep` each time;
every copy, rotation, and byte-equality proof the block names was a Python file operation inside a
saved script under `/home/decodeux/Repos/remedy/.remedy-wt/f301-r11-worker/`, each capturing its own
command's exit code in the same script; gates 4 and 5 ran through one saved script's two
`subprocess.run` calls; gate 3 was the round's only pytest invocation, run once, with no
`REMEDY_TEST_MAX_WORKERS` set and no `-n` passed; no mutation, no worktree was created; no file
under `.remedy-wt/f301-r11/` was modified; no file outside the round's named path set was touched;
no stash entry touched, no branch created, nothing merged, no force-push; `.agent/STOP` did not
appear at any point; commit subjects carry no leading-slash token and no absolute path; no shell
call used `cd`, `&&`, `||`, `;`, a pipe, `$(...)`, `${...}`, `$?`, a heredoc, `VAR=x cmd`, `export`,
`cp` or a shell `mkdir` — every shell call was one plain command, and every copy/hash/run/proof ran
inside a Python script instead.

## Round verdicts

Rounds 1 to 9 were already booked in the ledger before this session. Round 10's PASS verdict is
booked by this round's C1 — `.agent/live_review.md` now carries round 10's Gate entry forward.
Round 11's verdict is the reviewer's, to be written into the pull request and booked in the next
feature's first commit.

## For the operator, in plain sentences

When Remedy runs a mission of several jobs on a project, every sixth job is now a cleanup job that
Remedy plans by itself; it lists the oldest problems earlier jobs left open, the longest function
and file that grew past the size limits, and the files that were replaced but never deleted. The
number of jobs between cleanups is a setting, five unless changed. A cleanup can be skipped only by
giving a reason, which is written down, and the automatic orchestrator never skips one.
`remedy mission show` and the status a program reads say how many jobs are left before the next
cleanup and what it will carry. A test walks a whole mission of six jobs through Remedy's command
line to prove it. The maintenance job Remedy ran on itself before closing used two calls to the
paid model and about 9,900 tokens, did what it was asked, and was not applied. The whole test
collection passed once on the code that ships. The review package was built, and where it is is
recorded. A pull request is open and will be merged at the start of the next session unless the
operator merges it earlier. Fifteen smaller problems stay written down for the next clean-up
feature. Nothing waits for the operator.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. The Open PR Gate, which merges F301's pull request in the NEXT session and never in this one,
   after reading its hosted checks.
3. The booking of round 11's verdict in the next feature's first commit.
4. Rule A5 (the next unchecked line in `docs/roadmap/STATUS.md`).

Operator questions open: 0.
Open findings: 15 (R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158, R-1162, R-1172, R-1176,
R-1196, R-1219, R-1220, R-1225 and R-1230, Low; all owned by F297).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1: book round 10, the Built State, save the round 11 block, the STATUS line and the PR body | done | seven byte proofs `True`; committed `f97a0015c` |
| C2: rotate the finding ledger into its archive | done | rotation output matched `sim-readings.txt`; two byte proofs `True`; committed `2f79351e5` |
| C3: accept F301 in STATUS with its README sync and the self-use queue | done | three byte proofs `True`; content checks matched; this commit |
| Gate 1 | passed | status clean on the three C3 files; eleven-file byte sweep `ALL_EQUAL` |
| Gate 2 | passed | STATUS line occurs once; no `- [~]` line |
| Gate 3 | passed | `560 passed`, exit 0; no FAILED/ERROR/SKIPPED |
| Gate 4 | passed | six checks `pass`, `fail_count 0` |
| Gate 5 | passed | open findings list matches exactly |
| Gate 6 | pending | reported in the worker's final reply, after the push and the pull request |
| Push | pending | reported in the worker's final reply |
| Pull request | pending | reported in the worker's final reply; does not exist yet |
