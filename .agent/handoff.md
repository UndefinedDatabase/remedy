# Handback — F055 round 5 — book round 4, then the closure's evidence job and review package on the accepted head

## Session

SESSION 1 of feature F055 · round 5 · rounds so far 5

Context self-assessment: C1 and C2 landed clean on the first attempt with Gate 1 reading `ALL
True`, but A2's evidence job raised a producer-side refusal this session could not safely work
around within its own constraints (no second pytest run), so the round stops short of the
package it set out to build; the context budget stayed comfortable throughout.

Fortschritt: ~80 % (the block's record-keeping half, C1/C2, is done and pushed; the evidence job
is blocked on an unexplained pytest exit-1-with-zero-failures reading that the test-load rule
forbids re-running this round to diagnose, so the package, the closing round and everything after
A2 are not yet reachable) — Schätzung

## Range

Review of `d8bd1aafd`..`c667646e75be8570615e5acab8e6ac9ba58272ab` (then this commit).

## Commits

### `5e8dee0592caac84296b742516e9ab19d8391302` F055 R5 C1: book round 4, resolve R-1318, register R-1319, save the block
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r5.md` | +132/-0 | NEW: byte copy of `block.md` |
| `.agent/live_review.md` | +6/-0 | byte copy of `dry-live_review.md` (round 4 booked PASS, R-1318 resolved, R-1319 registered) |
| `.agent/plan.md` | +5/-6 | byte copy of `dry-plan.md` |

### `c667646e75be8570615e5acab8e6ac9ba58272ab` F055 R5 C2: save the evidence script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f055-r5-create_f055_evidence.py` | +376/-0 | NEW: byte copy of `create_f055_evidence.py`, the closure's evidence-bundle producer for this round, alone (no other path in this commit) |

C2 is the closure's ACCEPTED HEAD: full sha `c667646e75be8570615e5acab8e6ac9ba58272ab`.

### (this commit) F055 R5 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | full rewrite, per the block's non-zero-exit stop clause |

## External actions

- `git rev-parse HEAD` / `origin/feature/f055-rehearsal` both read `d8bd1aafd...` and
  `git status --porcelain` was empty before any write; no `.agent/STOP`. `git branch
  --show-current` read `feature/f055-rehearsal` immediately before every commit below.
- Push after C2: `git push -u origin feature/f055-rehearsal` — exit 0 on the first attempt (no
  HTTP 500, no retry needed): `d8bd1aafd..c667646e7  feature/f055-rehearsal -> feature/f055-rehearsal`.
- A1, the staging reclaim preview: `python3 -m apps.cli.main data reclaim --orphans`, exit 0.
  `Reclaimable: nothing` — no candidate listed, so `--apply` was skipped per the block's own
  instruction for that case. The one refused path, with its reason: `review_staging.n4o46eq_
  class_not_job_keyed: no job owns this path; reclaim addresses job-keyed classes only` (1.5 MB).
- A2, the evidence job: `git reflog -n 3 --date=iso` and `git branch --show-current` recorded
  (both quoted in Verification below), then `python3
  .agent/authored/f055-r5-create_f055_evidence.py .remedy-wt/f055-r5-evidence` launched detached
  from a Python wrapper (`cwd=/home/decodeux/Repos/remedy`), polled over roughly 17 minutes, whole
  output written to `/home/decodeux/Repos/remedy/.remedy-wt/f055-r5-worker/evidence.log`, exit code
  captured inside the wrapper to `/home/decodeux/Repos/remedy/.remedy-wt/f055-r5-worker/evidence.exit`.
  Result: **exit 1**. Per the block's non-zero-exit clause this round stops here: no A3 was
  attempted, and this handback is written and pushed instead.
- No `gh pr create/merge/edit`, no STATUS/README edit, no ledger rotation, no queue edit, no
  self-use run, no other provider call. `git reflog -n 3` and `git branch --show-current` were
  re-read after A2 (see Verification) — neither moved, so this is a clean stop rather than the
  block's "commit nothing more" branch (there was nothing more to lose either way: A2 commits
  nothing by design).
- Push after C3 follows this commit: `git push origin feature/f055-rehearsal`; its outcome is
  reported in the session's final reply (Gate 6), since it does not exist yet when this file is
  written.

## Verification

**Digests verified before anything else**, each with a Python sha256 reader: `block.md` 132 lines
/ `c67e60d3f6bf2d43c6ea8c665e7b8ec4a6527fcff2ac690d064bdc244027b662` — matched. All four other
prepared files' sha256 (`create_f055_evidence.py`, `dry-live_review.md`, `dry-plan.md`,
`verify.py`) matched the digests given in the prompt.

**Gate 1** — `git status --porcelain` empty, then
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f055-r5/prep/verify.py /home/decodeux/Repos/remedy c667646e75be8570615e5acab8e6ac9ba58272ab`:
```
True C1's single parent is d8bd1aafd
True C2's single parent is C1
True C1's subject begins 'F055 R5 C1:'
True C2's subject begins 'F055 R5 C2:'
True C1 .agent/authored/f055-r5.md equals block.md
True C1 .agent/live_review.md equals dry-live_review.md
True C1 .agent/plan.md equals dry-plan.md
True C1 names exactly its paths []
True C2 .agent/authored/f055-r5-create_f055_evidence.py equals create_f055_evidence.py
True C2 names exactly its paths []
True fork..C2 ancestry 25 plain 25, both 25
True at most one commit after C2 (0)
ALL True
```
One run, green.

**A1's reading** — quoted whole above in External actions; exit 0.

**A2's reading** — `git reflog -n 3 --date=iso` before launch:
```
c667646e7 HEAD@{2026-10-14 17:38:45 +0200}: commit: F055 R5 C2: save the evidence script
5e8dee059 HEAD@{2026-10-14 17:38:32 +0200}: commit: F055 R5 C1: book round 4, resolve R-1318, register R-1319, save the block
d8bd1aafd HEAD@{2026-10-14 17:32:08 +0200}: commit: F055 R4 C6: handback
```
`git branch --show-current`: `feature/f055-rehearsal`.

The job's whole output (`evidence.log`, all 15 lines, verbatim):
```
head c667646e75be8570615e5acab8e6ac9ba58272ab
ancestry-path count 25
plain count 25
collected node ids 8337, deselected 169
red control: unsafe among the real ids 0 []
red control: planted id -> a local absolute path
pytest exit 1, {'passed': 8328, 'failed': 0, 'skipped': 9}, output_hash 53f4899ddb44b2ef8198d76bc09ffc85bf519043de5067c20d139ce7a6cf5b35
Traceback (most recent call last):
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 376, in <module>
    sys.exit(main())
  File "/home/decodeux/Repos/remedy/.agent/authored/f055-r5-create_f055_evidence.py", line 348, in main
    summary = create_manual_completion_bundle(
  File "/home/decodeux/Repos/remedy/packages/orchestration/job_evidence.py", line 2826, in create_manual_completion_bundle
    raise ValueError("a recorded verification command failed; refusing to build a clean bundle")
ValueError: a recorded verification command failed; refusing to build a clean bundle
```
Wrapper exit code (`evidence.exit`): `1`.

Reading against the block's expectations: `head` equals C2's full sha — match. Ancestry 25 /
plain 25 — match. `collected node ids` 8337, `deselected` 169 — exactly the precheck's 8337, not
merely within a few of it. Red control `unsafe among the real ids 0 []` — match. Planted id
answers `a local absolute path` — match. The one mismatch is `pytest exit 0` expected versus
**exit 1** actual, which is what triggers this round's stop.

`git reflog -n 3 --date=iso` and `git branch --show-current` again, after A2: both identical to
the readings taken before launch (reflog's three entries unchanged, branch still
`feature/f055-rehearsal`); `git status --porcelain` empty. Neither moved.

**Every failed node id — could not be produced**, and the reason is stated precisely rather than
guessed at: the parsed counts (`passed=8328, failed=0, skipped=9`, summing exactly to the 8337
selected) carry no failure, yet pytest's own return code is 1, which pytest sets whenever
`session.testsfailed` is nonzero — a count that also rises on collection, setup or teardown
*errors*, not only on assertion failures. The evidence script's own summary-line regex
(`.agent/authored/f055-r5-create_f055_evidence.py:315-320`) only matches the words `passed`,
`failed` and `skipped`; it has no `error` bucket, so an error count would move the exit code
without appearing anywhere in the recorded counts. The actual pytest `-v` output that would show
which node id(s) errored (`run.stdout` inside that script, at its line 312-314) was held only in
that subprocess's own memory and was never written to any file before the process exited — it is
gone now. `.pytest_cache/v/cache/lastfailed` was read (a file inspection, not a second pytest
invocation) on the chance it had been refreshed by this run: its mtime is
`2026-10-14 17:27:50+02:00`, which **predates** this round's A2 launch and matches exactly the
timestamp F055 round 4's own closure-suite record already carries (`recorded
2026-10-14T15:27:50Z`), so its 88 entries belong to an earlier, unrelated session and reporting
them as this run's failures would misattribute stale data rather than inform. The test-load rule
(amend0930-test-load) forbids any further pytest command this round, so no rerun was attempted to
pin the real cause down. This is recorded as a deviation below rather than papered over.

**A3 — not attempted.** The block orders it "from the clean, pushed tree at C2" as a step that
follows A2; A2 did not reach a state A3 could build from.

**Gate 5 (integrity check + open-id listing)** — ordered "after A3, before C3". Run anyway, out of
its literal sequence, because it is read-only, costs nothing, and runs no test:
`python3 -m apps.cli.main integrity check --json`:
```
{"check_count": 6, "checks": [{"message": "handlers=188", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Then `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`:
```
['R-1246', 'R-1276', 'R-1277', 'R-1278', 'R-1279', 'R-1280', 'R-1281', 'R-1282', 'R-1283', 'R-1284', 'R-1285', 'R-1286', 'R-1287', 'R-1288', 'R-1289', 'R-1290', 'R-1291', 'R-1292', 'R-1293', 'R-1294', 'R-1295', 'R-1296', 'R-1297', 'R-1298', 'R-1299', 'R-1300', 'R-1301', 'R-1302', 'R-1303', 'R-1304', 'R-1305', 'R-1306', 'R-1307', 'R-1308', 'R-1309', 'R-1310', 'R-1311', 'R-1312', 'R-1313', 'R-1319']
```
40 ids: `R-1246`, then `R-1276` to `R-1313`, then `R-1319`, in order, as required. `git status
--porcelain` empty throughout. This is reported as informational — not as a completed Gate 5 —
because A3 never happened and the gate's own ordering names A3 as its precondition.

**Gate 6** — after this commit's push: reported in the session's final reply only, since it does
not exist yet when this file is written.

## Authored-text proofs

`.agent/authored/f055-r5.md` against `block.md`: byte-identical, sha256
`c67e60d3f6bf2d43c6ea8c665e7b8ec4a6527fcff2ac690d064bdc244027b662`, confirmed by my own copy
script at write time and again independently by `verify.py`'s Gate 1 check (`git show
<C1>:<path>` compared to the prep file's bytes — `True`). `.agent/live_review.md` against
`dry-live_review.md` and `.agent/plan.md` against `dry-plan.md` (both C1): each confirmed
byte-equal by a Python equality check at copy time and again by Gate 1's per-path check.
`.agent/authored/f055-r5-create_f055_evidence.py` against `create_f055_evidence.py` (C2):
byte-identical, confirmed the same two ways. No other reviewer-authored text was applied this
round.

## Deviations & assumptions

- **A2 exited non-zero (1) instead of the expected 0.** The block's own clause for this case was
  followed: this round stops, writes this handback with the log's tail (here, the whole 15-line
  log, since it is short) and pushes, rather than attempting A3 or C3's normal path. See
  Verification above for the full reading and the exact ValueError raised
  (`packages/orchestration/job_evidence.py:2826`, "a recorded verification command failed;
  refusing to build a clean bundle").
- **"Every failed node id" could not be produced.** The parsed verification counts show zero
  failures; pytest's exit code 1 most plausibly reflects a collection/setup/teardown *error*
  count that the evidence script's regex never captures, but the raw output that would name such
  a node id was never persisted and the test-load rule forbids a second pytest run this round to
  recover it. This is reported as an inability rather than guessed at — see Verification for the
  full reasoning, including why `.pytest_cache/v/cache/lastfailed`'s 88 stale entries (predating
  this run) are not reported as this run's failures.
- **A3 was not attempted** and **Gate 5's integrity/open-id check was run anyway, out of its
  literal "after A3" order**, purely because it is read-only and costs nothing; it is reported as
  informational, not as a completed gate, since A3 — its stated precondition — never happened.
- `.agent/plan.md` is not rewritten in C3: the block's C3 path list is `.agent/handoff.md` only,
  and that restriction is honoured here even though the plan's "Next Steps" line (written in C1,
  before A2 ran) now assumes a package that was not built. The accurate state lives in this
  handback instead.
- No other deviation: C1 and C2 matched the block exactly (Gate 1 `ALL True`), the push after C2
  needed no retry, and A1's reading was taken and reported exactly as ordered.

## For the operator, in plain sentences

No review package exists yet for this feature — the evidence-collection step that builds it ran
into an internal safety check refusing to certify a "clean" result, because the test run it was
grading returned a failing exit code while reporting zero failed tests, a contradiction nobody
has explained yet. No old scratch copies were cleaned up this round beyond the routine check,
which found one small 1.5 MB leftover it correctly left alone because it belongs to no job.
Nothing here needs you yet: the next session needs to read the full test output directly (rather
than the short summary this round could afford) to find out what actually went wrong before
anything is rebuilt.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The evidence job's exit-1-with-zero-failures contradiction needs a fresh, fully-captured pytest
   run (writing the complete output to disk before any parsing, not just holding it in memory) to
   identify what actually errored, since this round's one permitted run did not preserve enough
   detail to say.
4. Once that is understood and repaired, redo A2, then A3 (the review package), then the closing
   round: the Built State, the rotation, SU-064's `consumed_by`, the STATUS flip with the README
   sync, and the pull request, left unmerged.

Operator questions open: 0.
Open findings: 40 (R-1246, R-1276 to R-1313 and R-1319, all owned by F307).

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | Gate 1's checks `True`; 143 insertions |
| C2 | done | Gate 1's checks `True`; 376 insertions; full sha `c667646e75be8570615e5acab8e6ac9ba58272ab` is the accepted head |
| A1 | done | exit 0, `Reclaimable: nothing`, `--apply` skipped per the block's own rule for that case, one refused path reported |
| A2 | deviated | evidence job exited 1 instead of 0; stopped per the block's own non-zero-exit clause rather than proceeding to A3 |
| A3 | skipped | blocked by A2's non-zero exit; the block's precondition for A3 ("from the clean, pushed tree at C2" after a successful A2) was not met |
| C3 | done | this commit |
| Gate 1 | done | `ALL True`, one run |
| Gate 2 (A1) | done | empty reading and the one refused path recorded |
| Gate 3 (A2) | deviated | every line matched expectation except `pytest exit 1` where `pytest exit 0` was required |
| Gate 4 (A3) | skipped | A3 never ran |
| Gate 5 | deviated | run anyway out of order for visibility; `fail_count 0`, 40 open ids exactly as required, but not counted as a completed gate since A3 — its precondition — never happened |
| Gate 6 | done | reported in the reply, after this commit's push |
