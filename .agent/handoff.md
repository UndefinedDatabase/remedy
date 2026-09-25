# Handback — F024 Phase timeline with scrubber · Round 9 (CI repair)

## Session

SESSION 2 of feature F024 · round 9 · rounds so far 9

Ample context remained throughout this round; the round was a small, focused CI repair with no
surprises, and a large majority of the budget remained at the point this handback was written.

## Range

Review of 953d57153..HEAD

## Commits

### 482826211 F024 R9 C1: book round 8, register R-1048, copy the round's block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r9-block.md | +97/-0 | copy of this round's block, verbatim |
| .agent/authored/f024-r9-ledger.md | +4/-0 | copy of the ledger.md payload |
| .agent/authored/f024-r9-plan.md | +33/-0 | copy of the plan.md payload |
| .agent/authored/f024-r9-probe.py | +52/-0 | copy of the probe.py payload |
| .agent/authored/f024-r9-test_from.txt | +1/-0 | copy of the test_from.txt payload |
| .agent/authored/f024-r9-test_to.txt | +2/-0 | copy of the test_to.txt payload |
| .agent/live_review.md | +4/-0 | round 8's closing Gate entry and R-1048's registration appended, its `953d5715` bytes plus ledger.md |
| .agent/plan.md | +14/-9 | rewritten whole to the plan.md payload |

207 insertions, 9 deletions by `git show --numstat` — the block's stated expectation, this block's
own line count (97) plus 110 (4+33+52+1+2+4+14), matches exactly cell by cell against the tool;
well under the 500-insertion STOP threshold.

### 7a3948e12 F024 R9 C2: strip vitest's colour escapes before reading its summary (R-1048)
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_timeline_scrub_live.py | +2/-1 | test_from.txt's line (the plain `re.search` over `out`) replaced by test_to.txt's two lines (a comment naming R-1048, then the same search over `out` with vitest's colour escapes stripped first); FROM was present exactly once and absent afterward, TO present exactly once afterward; no production file touched |

2 insertions, 1 deletion by `git show --numstat`, that file alone — matches the block's stated
expectation exactly, cell by cell against the tool.

## External actions

- `git worktree add --detach .remedy-wt/f024-r9-g4 7a3948e1227e8cf00d5a39ce780fa0f8c891c3db` —
  succeeded, worktree prepared at detached HEAD `7a3948e12` (G4).
- `git worktree remove .remedy-wt/f024-r9-g4` — succeeded, worktree removed; `git worktree list`
  after removal no longer lists it (G4).
- `git push origin feature/f024-phase-timeline-scrubber` — not yet run at the point this handback
  is written; it runs immediately after this commit (C3), never force, and its outcome plus G5's
  readings are reported in the final reply only, since the handoff commit precedes the push.

No PR create, edit or merge this round (constraint 4: pull request 279 is left to the reviewer),
and no other `gh` command was run.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required — checked before step one)
```

```
$ (line count and sha256 of .remedy-wt/f024-r9/block.md, measured)
line_count: 97
sha256: b0ee9700647396c6ebc37aeebdc0121f91b71f2222b0754753db9bf716261d56
```
Matches both readings given in the delegation message exactly (97 lines, that sha256) — R-0954.

```
$ (lines/bytes/sha256 of each payload under .remedy-wt/f024-r9/)
ledger.md      lines=4  bytes=3564 sha256=2341d8942c7bee612f367e875a70822dab1403385ca1a4d796a3015774230865
plan.md        lines=33 bytes=1209 sha256=945048b323acfa52a57d5b785b763e67ad33cf976fd89964276b9fe395696fb6
test_from.txt  lines=1  bytes=63   sha256=193ba4a7a33c634e0888602138575d2ee8d7a2fc45fcf2b36829b40e090fbbdd
test_to.txt    lines=2  bytes=183  sha256=a9f2796f998db11a82a33f113957f0a1906a4d4a6701504f8f0ca28a6d3512c5
probe.py       lines=52 bytes=2153 sha256=982d88bb694f1cc634a7d77379241f818cf5e4ff6520c4b2de46b53cd7e47325
```
All 5 match the PAYLOADS table exactly (G1).

### G1 — transport + state
```
$ (python check: .agent/plan.md == plan.md payload; .agent/live_review.md == its 953d5715 bytes +
   ledger.md; each .agent/authored/f024-r9-* == its payload, block copy against block.md)
plan_ok: True
live_review_ok: True
authored_copies_ok: True
block_copy_ok: True
ALL: True
```
```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's text at C1
['R-1008', 'R-1048']
```
Matches the reviewer's simulation reading exactly, `['R-1008', 'R-1048']` (G1).

### G2 — the pair
```
$ (bytes/sha256 of tests/ui_server/test_timeline_scrub_live.py at C2)
bytes=3637 sha256=7a8287268b0af80542069274bfd8554fa7b21a5574eb20e1973389497c63cddc
```
Matches the block's G2 reading exactly. `git show --numstat` of C2 lists that file alone, 2/1
(shown above). test_from.txt count 0x, test_to.txt count 1x, confirmed by the replace script's own
assertions before writing.

### G3 — serial suite, ruff, integrity check
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_timeline_scrub_live.py \
  tests/cli/test_golden_path.py tests/orchestration/test_live_review_rotation.py \
  tests/orchestration/test_integrity_gate.py; echo "REAL_EXIT=$?"
........................................................................ [ 82%]
...............                                                          [100%]
87 passed in 57.33s
REAL_EXIT=0
```
87 passed, 0 failed, 0 skipped — the reviewer's sim worktree read 86 passed/1 skipped there (the
live scrub node skipping for want of `apps/ui/node_modules`); in the primary checkout that node
PASSED instead of skipping, matching the block's stated expectation of 87 passed exactly. No
SKIPPED line appears in the output — none to report.

```
$ python3 -m ruff check tests/ui_server/test_timeline_scrub_live.py; echo "REAL_EXIT=$?"
All checks passed!
REAL_EXIT=0
```

```
$ python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.

### G4 — red/green probe, disposable worktree
```
$ git worktree add --detach .remedy-wt/f024-r9-g4 7a3948e1227e8cf00d5a39ce780fa0f8c891c3db
Preparing worktree (detached HEAD 7a3948e12)
HEAD is now at 7a3948e12 F024 R9 C2: strip vitest's colour escapes before reading its summary (R-1048)

$ (python3 -B .../probe.py .../, run with cwd= the worktree, never `cd` the shell there)
EXIT 0
CONTROL the C2 file, CI unset | exit 0 | 1 passed in 3.89s | []
RED the old line, CI=true | exit 1 | 1 failed in 3.85s | ['FAILED tests/ui_server/test_timeline_scrub_live.py::test_a_live_jobs_ledger_scrubs_to_exac']
GREEN the C2 file, CI=true | exit 0 | 1 passed in 3.67s | []
restored byte-identical: True
link removed: True

$ git worktree remove .remedy-wt/f024-r9-g4
$ git worktree list
(primary; no f024-r9-g4 entry — removed; all other pre-existing worktrees, f015-*, f020-*, f023-*,
 f024-r1..r8 dry/sim, f024-r9-sim, f284-*, job-*, left untouched)
```
CONTROL exit 0/1 passed, RED exit 1/1 failed (the hosted run's own failing node), GREEN exit 0/1
passed, restored byte-identical True, link removed True — matches the reviewer's stated readings
against its sim tree exactly, line for line.

## Authored-text proofs

All 6 reviewer-authored payload copies under `.agent/authored/f024-r9-*` (the block copy, plus
`ledger.md`, `plan.md`, `probe.py`, `test_from.txt`, `test_to.txt`) were built with
`shutil.copyfile` from source to destination — never retyped, never edited — and compared byte for
byte against their sources by G1's python check: all BYTE-IDENTICAL. `.agent/plan.md` was rewritten
whole via `shutil.copyfile` from the plan.md payload — never retyped — and confirmed to match both
the PAYLOADS table digest and the payload's own bytes. `.agent/live_review.md` was built by
concatenating its `953d5715` bytes with `ledger.md`'s bytes, verified byte-identical against that
construction by G1's check.

`tests/ui_server/test_timeline_scrub_live.py` was rewritten by an exact `str.replace` of
test_from.txt's bytes with test_to.txt's bytes (both read from the committed payload files, never
retyped), guarded by asserted pre-conditions (FROM present exactly once, TO absent) before the
write; the result's bytes and sha256 matched the block's G2 table exactly.

## Deviations & assumptions

None. Both content commits landed in the block's stated order — C1, C2 — with no payload edited,
retyped or repaired, and no production file touched. G1 through G4 ran at C2, before this
handback, per the block's ordering; G5 runs after this handback is written and after the push, and
its readings go in the final reply, per the block's own note that the handoff commit precedes it.
The one worktree this round touched, `.remedy-wt/f024-r9-g4`, was created at C2 for G4 and removed
immediately after, per constraint 6 and the block's G4 instruction; every pre-existing worktree
(the reviewer's `.remedy-wt/f024-r9-sim`, the `f015-*`, `f020-*`, `f023-*`, `f024-r1`..`f024-r8`,
`f284-*` and `job-*` ones) and every stash were left untouched. No test was weakened or deleted to
pass; the repair strips colour escapes before the existing assertion, which is unchanged. No merge,
no comment, no edit on pull request 279 this round (constraint 4). No force-push.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 207 insertions, 9 deletions by `git show --numstat`, matches the block's expectation (97+110) exactly cell by cell |
| C2 | done | 2 insertions, 1 deletion by `git show --numstat`, that file alone, matches exactly |
| G1 | done | all 5 payload digests and 6 transport-identity checks matched; open_finding_ids read `['R-1008', 'R-1048']`, matching the reviewer's simulation |
| G2 | done | bytes=3637, sha256 matched; `git show --numstat` of C2 lists the file alone at 2/1 |
| G3 | done | 87 passed, 0 failed, 0 skipped (no SKIPPED line); ruff "All checks passed!"; integrity check 6/6 pass, fail_count 0 |
| G4 | done | CONTROL exit 0/1 passed, RED exit 1/1 failed, GREEN exit 0/1 passed, restored byte-identical True, link removed True; worktree added and removed cleanly |
| C3 | in progress | this handback being written now; the push follows immediately after this commit |
| G5 | pending | reported in the final reply, run after this handback is committed and pushed |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 9, and the Open PR Gate on
pull request 279 after its hosted CI re-runs on this push. Operator questions open: 3.
