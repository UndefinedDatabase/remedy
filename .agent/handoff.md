# Handback — F055 round 6 — book round 5, then the evidence job again on the new accepted head, and the review package

## Session

SESSION 1 of feature F055 · round 6 · rounds so far 6

Context self-assessment: the block's digests, C1's copy/commit/push and Gate 1 all landed clean
on the first attempt, and A1's single permitted pytest run read a genuine one-test failure (not
round 5's zero-failed, data-root anomaly) that this round's test-load rule forbids diagnosing
further this session, so the package (A2) and this round's closing steps were correctly not
attempted; the context budget stayed comfortable throughout.

Fortschritt: ~75 % (C1 is done and pushed, and A1 ran exactly once under the required isolation —
nothing else touched the repo while it ran — but it surfaced a REAL failing test rather than
round 5's zero-failed anomaly, so the package, the closing round and everything after A1 are not
yet reachable, and a real repair is now needed before the next attempt, not merely a clean rerun)
— Schätzung

## Range

Review of `397d93578`..`ed969049b851070ef38eb16209a24c4a1878e3db` (then this commit).

## Commits

### `ed969049b851070ef38eb16209a24c4a1878e3db` F055 R6 C1: book round 5 and the plan, save the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r6.md` | +123/-0 | NEW: byte copy of `block.md` |
| `.agent/live_review.md` | +2/-0 | byte copy of `dry-live_review.md` (books round 5's verdict) |
| `.agent/plan.md` | +3/-3 | byte copy of `dry-plan.md` |

C1 is the closure's ACCEPTED HEAD: full sha `ed969049b851070ef38eb16209a24c4a1878e3db`.

### (this commit) F055 R6 C2: handback with the evidence and package readings
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite, per the block's non-zero-exit stop clause under A1 |

## External actions

- Preconditions checked before any write: `git rev-parse HEAD` and `origin/feature/f055-rehearsal`
  both read `397d9357878a524042b8d247d9cf2a237b432223`; `git status --porcelain` was empty;
  `.agent/STOP` absent. `git branch --show-current` read `feature/f055-rehearsal` immediately
  before C1's commit.
- Push after C1: `git push -u origin feature/f055-rehearsal` — exit 0 on the first attempt (no
  HTTP 500, no retry needed): `397d93578..ed969049b  feature/f055-rehearsal -> feature/f055-rehearsal`.
- A1, the evidence job: `git reflog -n 3 --date=iso` and `git branch --show-current` recorded
  (quoted in Verification below), then `launch.py` started the evidence script detached
  (`python3 .agent/authored/f055-r5-create_f055_evidence.py .remedy-wt/f055-r6-evidence`, cwd
  `/home/decodeux/Repos/remedy`), and `wait.py evidence <log dir> 50` was run, and ONLY that, while
  it ran — no other command touched the repo for the full ~20-minute run. Result: **exit 1**
  (wall 1180.8 s). Per the block's non-zero-exit clause this round stops here: `load_record.py`
  was run once (its line quoted in Verification), A2 (the review package) was **not** attempted,
  and this handback is written and pushed instead.
- No `gh pr create/merge/edit`, no STATUS/README edit, no ledger rotation, no queue edit, no
  self-use run, no other provider call, no staging reclaim (round 5 already ran it and this
  round's block does not repeat it). `git reflog -n 3` and `git branch --show-current` were
  re-read after A1 (see Verification) — neither moved, so this is a clean stop (A1 commits
  nothing by design either way).
- Gate 4 (`integrity check` + open-id listing), ordered "after A2, before C2", was run anyway
  because it is read-only, costs no test run, and its reading is reported as informational below
  — not as a completed Gate 4, since A2, its stated precondition, never happened.
- Push after C2 follows this commit: `git push origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply (Gate 5), since it does not exist yet when this file is
  written.

## Verification

**Digests verified before anything else**, each with a Python sha256 reader: `block.md` 123
lines / `c3c025dcfb4eb7ba704216c07cd62c1fb6a5c4d9a0d43f9aff527fe74d832236` — matched. All six other
prepared files' sha256 (`dry-live_review.md`, `dry-plan.md`, `launch.py`, `wait.py`,
`load_record.py`, `verify.py`) matched the digests given in the prompt.

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r6/prep/verify.py /home/decodeux/Repos/remedy ed969049b851070ef38eb16209a24c4a1878e3db`:
```
True C1's single parent is 397d93578
True C1's subject begins 'F055 R6 C1:'
True C1 .agent/authored/f055-r6.md equals block.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True fork..C1 ancestry 27 plain 27, both 27
True at most one commit after C1 (0)
ALL True
```
One run, green.

**A1's reading** — `git reflog -n 3 --date=iso` before launch:
```
ed969049b HEAD@{2026-10-14 18:29:20 +0200}: commit: F055 R6 C1: book round 5 and the plan, save the block
397d93578 HEAD@{2026-10-14 18:07:00 +0200}: commit: F055 R5 C3: handback with the evidence and package readings
c667646e7 HEAD@{2026-10-14 17:38:45 +0200}: commit: F055 R5 C2: save the evidence script
```
`git branch --show-current`: `feature/f055-rehearsal`.

`launch.py`'s own line: `started evidence, wrapper pid 262854 log /home/decodeux/Repos/remedy/.remedy-wt/f055-r6-worker/evidence.txt`.

`wait.py`'s whole printed output (the job's full 15-line log, verbatim, plus the exit reading):
```
head ed969049b851070ef38eb16209a24c4a1878e3db
ancestry-path count 27
plain count 27
collected node ids 8337, deselected 169
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 1, {'passed': 8327, 'failed': 1, 'skipped': 9}, output_hash 2969acc3490283b465bde5c3048d11950b9139cffc59c8a15601223ad8625ea6
Traceback (most recent call last):
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 376, in <module>
    sys.exit(main())
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 348, in main
    summary = create_manual_completion_bundle(
  File "/home/decodeux/Repos/remedy/packages/orchestration/job_evidence.py", line 2826, in create_manual_completion_bundle
    raise ValueError("a recorded verification command failed; refusing to build a clean bundle")
ValueError: a recorded verification command failed; refusing to build a clean bundle
exit 1 wall 1180.8
```

Reading against the block's expectations: `head` equals C1's full sha — match. Ancestry 27 /
plain 27 — match. `collected node ids` 8337, `deselected` 169 — exact match. Red control
`unsafe among the real ids 0 []` — match. Planted id answers `a local absolute path` — match.
The mismatches: `pytest exit 0` expected versus **exit 1** actual, and `failed 0` expected versus
**`failed: 1`** actual — this is a REAL failing test this round, unlike round 5's `failed: 0`
reading with the same exit code. This is what triggers this round's stop.

`load_record.py`'s one printed line (run once, read-only):
```
{'collected': 8337, 'cpu_seconds': 1054.15, 'exit_status': 1, 'utc': '2026-10-14T16:49:23Z', 'wall_seconds': 1168.97, 'workers': 1}
```
Per the script's own docstring, `exit_status` 1 here means "a test failed or a process was left
behind" (as opposed to 0, which would mean the data-root guard of `tests/conftest.py` flipped the
exit code after the record was written — round 5's reading). This confirms round 6's failure is
a genuine one, not a repeat of round 5's anomaly.

`git reflog -n 3 --date=iso` and `git branch --show-current` again, after A1: both identical to
the readings taken before launch (same three entries, branch still `feature/f055-rehearsal`);
`git status --porcelain` empty. Neither moved, so nothing extra needs to be rolled back.

The evidence directory `/home/decodeux/Repos/remedy/.remedy-wt/f055-r6-evidence` exists (created
by the script's own `mkdir`) but is EMPTY (no `*_gate.json`, no `verification_tests.json` — the
`ValueError` fired before `create_manual_completion_bundle` wrote anything), so there is no
partial evidence on disk to clean up or to mistake for a result.

**Which node id failed — could not be produced**, for the same structural reason round 5
recorded: the evidence script's regex only extracts the `passed`/`failed`/`skipped` counts from
pytest's summary; the full `-v` output (`run.stdout` inside that script) that would name the
failing node id was held only in that subprocess's memory and was never written to disk before
the process exited. The test-load rule (amend0930-test-load) forbids any further pytest command
this round, so no rerun was attempted to identify it.

**A2 (the review package) — not attempted**, per the block's A1 non-zero-exit clause ("do not run
A2"). The block's A2 instructions (package name, SHA-256, `committed_review_subject`
base/head, `zipfile` checks, directory) therefore have no readings this round.

**Gate 4 (integrity check + open-id listing)** — ordered "after A2, before C2". Run anyway, out
of its literal sequence, because it is read-only, costs nothing, and runs no test:
`python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Then `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1319']
```
40 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1319`, in order, as required. `git status
--porcelain` empty throughout. Reported as informational — not as a completed Gate 4 — because
A2 never happened and the gate's own ordering names A2 as its precondition.

**Gate 5** — after this commit's push: reported in the session's final reply only, since it does
not exist yet when this file is written.

## Authored-text proofs

`.agent/authored/f055-r6.md` against `block.md`: byte-identical, sha256
`c3c025dcfb4eb7ba704216c07cd62c1fb6a5c4d9a0d43f9aff527fe74d832236`, confirmed by my own copy
script at write time and again independently by `verify.py`'s Gate 1 check (`git show
<C1>:<path>` compared to the prep file's bytes — `True`). `.agent/live_review.md` against
`dry-live_review.md` and `.agent/plan.md` against `dry-plan.md` (both C1): each confirmed
byte-equal by a Python equality check at copy time and again by Gate 1's per-path check. No other
reviewer-authored text was applied this round.

## Deviations & assumptions

- **A1 exited non-zero (1) with a REAL failing test** (`failed: 1`, confirmed by
  `load_record.py`'s `exit_status: 1` reading, "a test failed or a process was left behind"),
  rather than round 5's `failed: 0` / exit-1 anomaly the block's own preamble describes. The
  block's non-zero-exit clause under A1 was followed exactly: `load_record.py` run once and its
  line reported, A2 not attempted, this handback written with the log's tail and pushed, then
  stop.
- **Which node id failed could not be produced** — see Verification for the full reasoning: the
  evidence script never persists pytest's full `-v` output to disk, only the regex-derived
  counts, and the test-load rule forbids a second pytest run this round to recover it.
- **The evidence job id, package name, SHA-256, directory and `committed_review_subject`
  base/head that C2's instructions ask to be quoted from "the tool's own output line"** have no
  such readings: A2 never ran, and A1's script never prints its own `job_id` (`f055r5e1001`,
  visible only in the script's source, not in any output line) before raising. Reporting the
  source-level job id as if it were a tool output line would misrepresent the citation
  requirement, so it is named here as unavailable rather than substituted.
- **Gate 4 was run anyway, out of its literal "after A2" order**, purely because it is read-only
  and costs nothing; it is reported as informational, not as a completed gate, since A2 — its
  stated precondition — never happened.
- No other deviation: C1 matched the block exactly (Gate 1 `ALL True`), the push after C1 needed
  no retry, and A1 ran under the required isolation (reflog and branch unchanged before and
  after; nothing else ran while it was in flight).

## For the operator, in plain sentences

No review package was built this round: the evidence job's one permitted pytest run came back
with a real failing test, which is a different and more serious result than the first attempt in
the round before, which stopped only because something changed Remedy's own data folder while
the tests were running. This attempt ran with nothing else running at all, and still came back
with one test failing, so the data-folder explanation does not apply here. Nothing waits for you.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 6 and books its verdict in the next round's first commit.
4. The closing round: the Built State, the rotation, SU-064's `consumed_by`, the STATUS flip with
   the README sync, and the pull request, left unmerged.

Operator questions open: 0.
Open findings: 40 (R-1246, R-1276 to R-1313 and R-1319, all owned by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's checks `True`; full sha `ed969049b851070ef38eb16209a24c4a1878e3db` is the accepted head |
| A1 | deviated | evidence job exited 1 with a real failing test (`failed: 1`), not round 5's zero-failed anomaly; stopped per the block's own non-zero-exit clause |
| A2 | skipped | blocked by A1's non-zero exit; the block's own clause orders "do not run A2" in this case |
| C2 | done | this commit |
| Gate 1 | done | `ALL True`, one run |
| Gate 2 (A1) | deviated | every reading matched expectation except `pytest exit 1` (vs required 0) and `failed 1` (vs required 0) |
| Gate 3 (A2) | skipped | A2 never ran |
| Gate 4 | deviated | run anyway out of order for visibility; `fail_count 0`, 40 open ids exactly as required, but not counted as a completed gate since A2 — its precondition — never happened |
| Gate 5 | done | reported in the reply, after this commit's push |
