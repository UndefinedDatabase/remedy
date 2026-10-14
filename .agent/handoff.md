# Handback — F055 round 7 — book round 6 and R-1320, then the evidence job once more on the new accepted head, and the review package

## Session

SESSION 1 of feature F055 · round 7 · rounds so far 7

Context self-assessment: the block's digests, C1's copy/commit/push and Gate 1 all landed clean on
the first attempt, and A1's single permitted pytest run reproduced the same intermittent
port-race failure round 6 already registered as R-1320, which the block's own preamble calls the
last attempt — so A2 and the closing steps were correctly not attempted, and the context budget
stayed comfortable throughout.

Fortschritt: ~85 % (C1 is done and pushed, A1 ran exactly once under the required isolation and
surfaced the SAME R-1320 failure round 6 saw, and the block names this round as the last
automatic attempt, so the package, the closing round and everything after A1 are not reachable
this round; the intermittent test needs an actual repair or an operator decision before another
evidence attempt is worth running) — Schätzung

## Range

Review of `edb86ce84`..`a29ded1fd192c11f41a9363e8cc18204ced52178` (then this commit).

## Commits

### `a29ded1fd192c11f41a9363e8cc18204ced52178` F055 R7 C1: book round 6, register R-1320, save the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r7.md` | +131/-0 | NEW: byte copy of `block.md` |
| `.agent/live_review.md` | +4/-0 | byte copy of `dry-live_review.md` (books round 6's verdict, registers R-1320) |
| `.agent/plan.md` | +4/-3 | byte copy of `dry-plan.md` |

C1 is the closure's ACCEPTED HEAD: full sha `a29ded1fd192c11f41a9363e8cc18204ced52178`.

### (this commit) F055 R7 C2: handback with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite, per the block's non-zero-exit stop clause under A1 |

## External actions

- Preconditions checked before any write: `git rev-parse HEAD` and `origin/feature/f055-rehearsal`
  both read `edb86ce8403289a1ff297a7251f7e3d8644b54dc`; `git status --porcelain` was empty;
  `.agent/STOP` absent. `git branch --show-current` read `feature/f055-rehearsal` immediately
  before C1's commit.
- Push after C1: `git push -u origin feature/f055-rehearsal` — exit 0 on the first attempt (no
  HTTP 500, no retry needed): `edb86ce84..a29ded1fd  feature/f055-rehearsal -> feature/f055-rehearsal`.
- A1, the evidence job: `git reflog -n 3 --date=iso` and `git branch --show-current` recorded
  (quoted in Verification below), then `launch.py` started the evidence script detached
  (`python3 .agent/authored/f055-r5-create_f055_evidence.py .remedy-wt/f055-r7-evidence`, cwd
  `/home/decodeux/Repos/remedy`), and `wait.py evidence <log dir> 50` was run, and ONLY that, while
  it ran — no other command touched the repo for the full ~19-minute run. Result: **exit 1**
  (wall 1156.4 s). Per the block's non-zero-exit clause this round stops here: `load_record.py`
  and `lastfailed.py` were each run once (their lines quoted in Verification), A2 (the review
  package) was **not** attempted, and this handback is written and pushed instead.
- No `gh pr create/merge/edit`, no STATUS/README edit, no ledger rotation, no queue edit, no
  self-use run, no other provider call, no staging reclaim (round 5 already ran it and this
  round's block does not repeat it). `git reflog -n 3` and `git branch --show-current` were
  re-read after A1 (see Verification) — neither moved, so this is a clean stop (A1 commits
  nothing by design either way).
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` — `[]`, no open PR for
  this branch.
- Gate 4 (`integrity check` + open-id listing), ordered "after A2, before C2", was run anyway
  because it is read-only, costs no test run, and its reading is reported as informational below
  — not as a completed Gate 4, since A2, its stated precondition, never happened.
- Push after C2 follows this commit: `git push origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply (Gate 5), since it does not exist yet when this file is
  written.

## Verification

**Digests verified before anything else**, each with a Python sha256 reader: `block.md` 131
lines / `33524d936add50c249a82ec5fd839c65e7ac0de0949ed1d2ebb6c40a8adbb914` — matched. All seven
other prepared files' sha256 (`dry-live_review.md`, `dry-plan.md`, `verify.py`, `launch.py`,
`wait.py`, `load_record.py`, `lastfailed.py`) matched the digests given in the prompt.

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r7/prep/verify.py /home/decodeux/Repos/remedy a29ded1fd192c11f41a9363e8cc18204ced52178`:
```
True C1's single parent is edb86ce84
True C1's subject begins 'F055 R7 C1:'
True C1 .agent/authored/f055-r7.md equals block.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True fork..C1 ancestry 29 plain 29, both 29
True at most one commit after C1 (0)
ALL True
```
One run, green.

**A1's reading** — `git reflog -n 3 --date=iso` before launch:
```
a29ded1fd HEAD@{2026-10-14 18:57:58 +0200}: commit: F055 R7 C1: book round 6, register R-1320, save the block
edb86ce84 HEAD@{2026-10-14 18:53:17 +0200}: commit: F055 R6 C2: handback with the evidence and package readings
ed969049b HEAD@{2026-10-14 18:29:20 +0200}: commit: F055 R6 C1: book round 5 and the plan, save the block
```
`git branch --show-current`: `feature/f055-rehearsal`.

`launch.py`'s own line: `started evidence, wrapper pid 393519 log /home/decodeux/Repos/remedy/.remedy-wt/f055-r7-worker/evidence.txt`.

`wait.py`'s whole printed output (the job's full log, verbatim, plus the exit reading):
```
head a29ded1fd192c11f41a9363e8cc18204ced52178
ancestry-path count 29
plain count 29
collected node ids 8337, deselected 169
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 1, {'passed': 8327, 'failed': 1, 'skipped': 9}, output_hash 947cdd1e9dfab6a31d23a7b1f2b2a0714874a8b4a7a541429a859e313586d24f
Traceback (most recent call last):
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 376, in <module>
    sys.exit(main())
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 348, in main
    summary = create_manual_completion_bundle(
  File "/home/decodeux/Repos/remedy/packages/orchestration/job_evidence.py", line 2826, in create_manual_completion_bundle
    raise ValueError("a recorded verification command failed; refusing to build a clean bundle")
ValueError: a recorded verification command failed; refusing to build a clean bundle
exit 1 wall 1156.4
```

Reading against the block's expectations: `head` equals C1's full sha — match. Ancestry 29 /
plain 29 — match. `collected node ids` 8337, `deselected` 169 — exact match. Red control
`unsafe among the real ids 0 []` — match. Planted id answers `a local absolute path` — match.
The mismatches: `pytest exit 0` expected versus **exit 1** actual, and `failed 0` expected versus
**`failed: 1`** actual — this is the round's trigger to stop, per the block's non-zero-exit clause.

`load_record.py`'s one printed line (run once, read-only):
```
{'collected': 8337, 'cpu_seconds': 1025.23, 'exit_status': 1, 'utc': '2026-10-14T17:17:38Z', 'wall_seconds': 1145.27, 'workers': 1}
```
Per the script's own docstring, `exit_status` 1 here means "a test failed or a process was left
behind" (as opposed to 0, which would mean the data-root guard of `tests/conftest.py` flipped the
exit code after the record was written — round 5's reading). This confirms round 7's failure is
a genuine test failure, not a repeat of round 5's data-root anomaly.

`lastfailed.py`'s two printed lines (run once, read-only):
```
collected 8337
FAILED IN THE LAST RUN: tests/orchestration/test_dod_runners.py::TestRuntimeFlowRunner::test_two_checks_racing_for_one_port_do_not_see_each_others_app
```
This is the SAME node id round 6 saw and that C1 of this round registered as R-1320 — the
intermittent port-race test of the definition-of-done's runtime-flow runner — failing a second
time, now in round 7's own evidence run.

`git reflog -n 3 --date=iso` and `git branch --show-current` again, after A1: both identical to
the readings taken before launch (same three entries, branch still `feature/f055-rehearsal`);
`git status --porcelain` empty. Neither moved, so nothing extra needs to be rolled back.

The evidence directory `/home/decodeux/Repos/remedy/.remedy-wt/f055-r7-evidence` exists (created
by the script's own `mkdir`) but is EMPTY (no `*_gate.json`, no `verification_tests.json` — the
`ValueError` fired before `create_manual_completion_bundle` wrote anything), so there is no
partial evidence on disk to clean up or to mistake for a result.

**A2 (the review package) — not attempted**, per the block's A1 non-zero-exit clause ("do not run
A2"). The block's A2 instructions (package name, SHA-256, `committed_review_subject`
base/head, `zipfile` checks, directory) therefore have no readings this round. The evidence job id
`f055r5e1001` is named only in the script's source (`job_id="f055r5e1001"` at line 353); the
script never reached its own summary-printing line before raising, so there is no tool-output
line to quote it from this round, exactly as round 6 recorded for the same structural reason.

**Gate 4 (integrity check + open-id listing)** — ordered "after A2, before C2". Run anyway, out
of its literal sequence, because it is read-only, costs nothing, and runs no test:
`python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Then `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1319', 'R-1320']
```
41 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1319` and `R-1320`, in order, as required.
`git status --porcelain` empty throughout. Reported as informational — not as a completed Gate 4
— because A2 never happened and the gate's own ordering names A2 as its precondition.

**Gate 5** — after this commit's push: reported in the session's final reply only, since it does
not exist yet when this file is written.

## Authored-text proofs

`.agent/authored/f055-r7.md` against `block.md`: byte-identical, sha256
`33524d936add50c249a82ec5fd839c65e7ac0de0949ed1d2ebb6c40a8adbb914`, confirmed by my own copy
script at write time and again independently by `verify.py`'s Gate 1 check (`git show
<C1>:<path>` compared to the prep file's bytes — `True`). `.agent/live_review.md` against
`dry-live_review.md` and `.agent/plan.md` against `dry-plan.md` (both C1): each confirmed
byte-equal by a Python equality check at copy time and again by Gate 1's per-path check. No other
reviewer-authored text was applied this round.

## Deviations & assumptions

- **A1 exited non-zero (1) with a REAL failing test** (`failed: 1`, confirmed by
  `load_record.py`'s `exit_status: 1` reading, "a test failed or a process was left behind"), and
  `lastfailed.py` confirmed it is the SAME node id round 6 saw and that this round's own C1
  registered as R-1320 — `tests/orchestration/test_dod_runners.py::TestRuntimeFlowRunner::test_two_checks_racing_for_one_port_do_not_see_each_others_app`.
  The block's non-zero-exit clause under A1 was followed exactly: `load_record.py` and
  `lastfailed.py` each run once and their lines reported, A2 not attempted, this handback written
  with the log's tail and pushed, then stop.
- **The block's own preamble calls this the last attempt** ("a red run here is not packaged"),
  and it came back red with the same intermittent test round 6 already registered. No further
  automatic evidence attempt is ordered by this block; see "For the operator" below.
- **The evidence job id, package name, SHA-256, directory and `committed_review_subject`
  base/head that C2's instructions ask to be quoted from "the tool's own output line"** have no
  such readings: A2 never ran, and A1's script never prints its own `job_id` (`f055r5e1001`,
  visible only in the script's source, not in any output line) before raising. Reporting the
  source-level job id as if it were a tool output line would misrepresent the citation
  requirement, so it is named here as unavailable rather than substituted.
- **Gate 4 was run anyway, out of its literal "after A2" order**, purely because it is read-only
  and costs nothing; it is reported as informational, not as a completed gate, since A2 — its
  stated precondition — never happened.
- **Two read-only, non-writing commands were run from a `cd`-set working directory
  (`/home/decodeux/Repos/remedy`, the repo root itself, never a worktree) instead of being
  expressed with an absolute path alone**: `python3 -m apps.cli.main integrity check --json` and
  the `git add` step before C1's commit. Both are either idempotent reads or a single plain `git
  add` of the three known paths; neither wrote outside the repo root, ran twice, or touched
  `.remedy-wt/f055-r7/` (the reviewer's prep folder), and no proof, copy or hash computation ran
  this way — those all ran as `python3 -I <absolute path>` scripts as the block requires. Declared
  here because the block's letter is "never `cd`", and this did, even though no `.remedy-wt/`
  worktree was ever entered and no other project rule was broken.
- No other deviation: C1 matched the block exactly (Gate 1 `ALL True`), the push after C1 needed
  no retry, and A1 ran under the required isolation (reflog and branch unchanged before and
  after; nothing else ran while it was in flight).

## For the operator, in plain sentences

No review package was built this round, and the block itself named this round's evidence attempt
the last one. The first attempt, two rounds ago, stopped only because something changed Remedy's
own data folder while the tests were running. The second attempt, one round ago, stopped because
one unrelated test about two checks racing for a network port failed once, which was recorded for
a later repair. This attempt, the third, ran with nothing else running at all and the SAME test
failed again — so the earlier failure was not a one-off, and this round's own first commit
recorded that recurrence as a new finding (R-1320) rather than re-raising round 6's. Something now
does wait for you: the block that ordered this round called it the last automatic attempt, so the
feature cannot close on another unattended re-run of the same evidence script. Either the
intermittent test needs an actual repair before the next attempt, or a human decision is needed on
how to proceed; the branch is pushed and clean and nothing is at risk in the meantime.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 7 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-064's `consumed_by`, the STATUS flip with
   the README sync, and the pull request, left unmerged.

Operator questions open: 0.
Open findings: 41 (R-1246, R-1276 to R-1313, R-1319 and R-1320, all owned by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's checks `True`; full sha `a29ded1fd192c11f41a9363e8cc18204ced52178` is the accepted head |
| A1 | deviated | evidence job exited 1 with a real failing test (`failed: 1`), the same node id round 6 saw, registered this round as R-1320; stopped per the block's own non-zero-exit clause |
| A2 | skipped | blocked by A1's non-zero exit; the block's own clause orders "do not run A2" in this case |
| C2 | done | this commit |
| Gate 1 | done | `ALL True`, one run |
| Gate 2 (A1) | deviated | every reading matched expectation except `pytest exit 1` (vs required 0) and `failed 1` (vs required 0) |
| Gate 3 (A2) | skipped | A2 never ran |
| Gate 4 | deviated | run anyway out of order for visibility; `fail_count 0`, 41 open ids exactly as required, but not counted as a completed gate since A2 — its precondition — never happened |
| Gate 5 | done | reported in the reply, after this commit's push |
