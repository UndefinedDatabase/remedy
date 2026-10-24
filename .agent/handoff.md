# Handoff — F157 round 11 (the closing round: book round 10, accept F157, open the pull request)

## Session

SESSION 3 of feature F157 · round 11 · rounds so far 11. This closing round carried every gate and
commit of its block using only the verified prep bundle, and context stayed comfortably within
budget throughout. The session ends here because F157 is closed and the next feature starts in a
fresh session.

Fortschritt: 100 % (F157 is accepted; its pull request waits for the next session's Open PR Gate) — Schätzung.

## Range

Review of `e10ad0dc7`..`d76967845` (C1 and C2; C3 — the three files below plus this handoff — is
the commit that carries this file, per the handback template's self-reference exception).

## Commits

### 2485351cb F157 R11 C1: book round 10, the Built State, save the round 11 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r11.md` | +140/-0 | NEW FILE — this round's block, the authored-text proof |
| `.agent/authored/f157-r11-pr_body.md` | +77/-0 | NEW FILE — the pull request's body, the authored-text proof |
| `.agent/live_review.md` | +2/-0 | books round 10's PASS verdict (Gate: F157 R10) |
| `docs/roadmap/features/T8_F157.md` | +51/-0 | the feature file's Built State |
| `.agent/plan.md` | +4/-7 | rewritten: Current Step → round 11's closing sequence, Next Steps → the next session's merge and Rule A5 |

### d76967845 F157 R11 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-38 | rotated out: resolved records and old gate entries moved to the archive |
| `.agent/live_review_archive.md` | +38/-0 | rotated in: the same 38 records, now archived |

### (this commit) F157 R11 C3: accept F157 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F157's `[~]` line becomes `[x]`, accepted with its evidence job and package |
| `README.md` | +8/-2 | `163 of 316`, Tier 8 row `3 \| 13`, Tier 8 list gains F157's entry after F315's |
| `scripts/self_use_queue.json` | +1/-1 | SU-081's `consumed_by` becomes `F157` |
| `.agent/handoff.md` | rewritten | this file — carried in the same commit as C3's three files, per the handback template's self-reference exception (R-0149): a handoff cannot table the commit that writes it |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` (precondition check,
before any write) → `[]`. No push and no pull-request action yet this round: `git push origin
feature/f157-capability-matrix` runs once, immediately after this commit, per the block's THEN
step; `gh pr create` follows it, and names no pull request number here because none exists yet.
`gh pr list` runs once more after that, expected to hold exactly the one new pull request. No
worktree created or removed; no stash entry touched; no provider call.

## Verification

**Gate 1.** `git status --porcelain` (after placing C3's three files, before staging) → only the
three C3 files modified, exit 0. Then `python3 .remedy-wt/f157-r11/prep/verify.py .` → every check
line `True` except `absent	C3 committed` (expected — C3 had not been committed yet when the gate
ran), last line `ALL True`. Full output:

```
True	2485351cb single parent equal to the commit before it
True	d76967845 single parent equal to the commit before it
True	every commit carries a F157 R11 Cn subject: 2 of 2
True	on feature/f157-capability-matrix
True	C1 paths exactly the manifest's: ['.agent/authored/f157-r11-pr_body.md', '.agent/authored/f157-r11.md', '.agent/live_review.md', '.agent/plan.md', 'docs/roadmap/features/T8_F157.md']
True	C1 .agent/authored/f157-r11-pr_body.md numstat 77 0 equals 77 0
True	C1 .agent/authored/f157-r11-pr_body.md equals c1-.agent__authored__f157-r11-pr_body.md
True	C1 .agent/authored/f157-r11.md numstat 140 0 equals 140 0
True	C1 .agent/authored/f157-r11.md equals c1-.agent__authored__f157-r11.md
True	C1 .agent/live_review.md numstat 2 0 equals 2 0
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md numstat 4 7 equals 4 7
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 docs/roadmap/features/T8_F157.md numstat 51 0 equals 51 0
True	C1 docs/roadmap/features/T8_F157.md equals c1-docs__roadmap__features__T8_F157.md
True	C2 paths exactly the manifest's: ['.agent/live_review.md', '.agent/live_review_archive.md']
True	C2 .agent/live_review.md numstat 0 38 equals 0 38
True	C2 .agent/live_review.md equals c2-.agent__live_review.md
True	C2 .agent/live_review_archive.md numstat 38 0 equals 38 0
True	C2 .agent/live_review_archive.md equals c2-.agent__live_review_archive.md
absent	C3 committed
True	C3 working tree README.md equals c3-README.md
True	C3 working tree docs/roadmap/STATUS.md equals c3-docs__roadmap__STATUS.md
True	C3 working tree scripts/self_use_queue.json equals c3-scripts__self_use_queue.json
ALL True
```

**Gate 2.** A script read the prep folder's `status_line.txt`, stripped its one trailing newline,
and counted the result inside `docs/roadmap/STATUS.md`:

```
content repr (first 120 chars): '- [x] F157 — Capability matrix & honest degradation (T001–T003 complete; accepted 2026-10-24 · live review PASS — ACCEPT'
content length: 400
occurrences of content in STATUS.md: 1
number of lines in content: 1
lines beginning with '- [~]': []
GATE2_OK
```

Exit 0; the line occurs exactly once, and no line of it begins `- [~]`.

**Gate 3.** `python3 .remedy-wt/f157-r11/prep/gate3.py .`, run once:

```
exit 0
859 passed in 85.28s (0:01:25)
NOTICE ...................................................................      [100%]R-1411: 3 entries of the configured data root ~/Repos/remedy/.data changed in the folders a supervisor this run did not start and its clients write; not counted: ['api/calls.jsonl', 'projects/901d6b75-c848-48
integrity exit 0 6 pass; ['{"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}']
```

Exit 0, `859 passed` — the same passed count as `sim-gate3.txt`'s second line (seconds differ, as
the block allows); no `FAILED`, `ERROR` or `SKIPPED` line. The `NOTICE` line (truncated at 300
characters by `gate3.py`'s own print statement, and with this machine's home folder written as `~`
here) names a foreign process that wrote into the shared data root during the run, in the
conftest's own words (F151 D6). Gate 3 exited 0, not 1, so the one documented re-run exception for
a red gate 3 does not apply.

**Gate 4.** Bundled in gate 3's own output above: `integrity exit 0` and `"fail_count": 0`,
matching `sim-gate3.txt` exactly.

**Gate 5.**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450']`, exit 0 —
exactly the eight ids the block names.

## Rotation

`python3 scripts/rotate_live_review.py`, run once from the primary checkout, exit 0:

```
gate records moved: 9
finding pairs moved: 4 (8 records)
resolved-text records moved: 0
old ledger size: 168403 bytes
new ledger size: 143283 bytes
old archive size: 7320328 bytes
new archive size: 7345448 bytes
open findings before: 8
open findings after: 8
gate headers matching neither known form (left in place): 1
written: ~/Repos/remedy/.agent/live_review.md and ~/Repos/remedy/.agent/live_review_archive.md
```

Matches `sim-rotation.txt`'s lines 1–10 exactly (its own `written:` line differs only in the
sim worktree's path, as expected). Ledger size before: 168403 bytes; after: 143283 bytes. Archive
size before: 7320328 bytes; after: 7345448 bytes. Both resulting files were then proved byte-equal
to the prepared `c2-.agent__live_review.md` and `c2-.agent__live_review_archive.md`.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f157-r11-worker/copy_c1.py`, proved by `prove_c1.py`) read
`bytes_equal` for all five targets immediately after copying: `.agent/authored/f157-r11.md`,
`.agent/authored/f157-r11-pr_body.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/features/T8_F157.md`. Gate 1's `verify.py` run independently re-confirmed every
`C1 ... equals c1-...` line `True`.

C2's rotation output and both resulting ledger files were proved byte-equal to the prepared
`c2-.agent__live_review.md` and `c2-.agent__live_review_archive.md` disk-to-disk
(`.remedy-wt/f157-r11-worker/prove_c2.py`), independently re-confirmed by gate 1's `verify.py`.

C3's byte copy (`.remedy-wt/f157-r11-worker/copy_c3.py`, proved by `prove_c3.py`) read
`bytes_equal` for all three targets: `docs/roadmap/STATUS.md`, `README.md`,
`scripts/self_use_queue.json`, independently re-confirmed by gate 1's `verify.py` (the `C3 working
tree ... equals c3-...` lines).

The STATUS line: `docs/roadmap/STATUS.md` now reads, byte-identical to the prep folder's
`status_line.txt` without its trailing newline —
`- [x] F157 — Capability matrix & honest degradation (T001–T003 complete; accepted 2026-10-24 ·
live review PASS — ACCEPTED · Evidence job f157r10e1001 · package
remedy-review-20261024-070450-READY_FOR_REVIEW.zip · SHA-256
9486e587f096ea0811f1d4b65439c0b4ee1bbc648e623f4a037dd73adff72403 · package path
~/Repos/remedy-history/zips · accepted HEAD ce081c649130009560b1cfc9c3ccd26b16641cfb)` —
occurring exactly once in the file, confirmed by gate 2.

## Deviations & assumptions

None. C1, C2 and C3 ran exactly as the block orders, in the order it gives; all five gates read
green on the first and only run of each; gate 3's `NOTICE` line is informational under DECISION
F151 D6 and did not trigger its re-run exception because gate 3 exited 0, not 1.

## For the operator, in plain sentences

Remedy now keeps one list of what each feature needs a model to be able to do, and what it does
instead when the model cannot do it. Every such choice goes through that one place, and a test
fails if any other code asks a model about its abilities anywhere else. A run now writes down
every fallback it used, and the run's report, the job's report and the worker description each
show a line naming it. Earlier, the paid run on this project itself wrote the first tests for the
part of Remedy that hides secrets in public text; its reviewer passed that work, but it is kept
unapplied, and the fake test secrets inside the copy kept in the records are blanked out. The
whole test collection passed on the code that ships, and it used a little more computer time than
the last time it was measured. The review package is named
`remedy-review-20261024-070450-READY_FOR_REVIEW.zip` and lives in the zips folder under this
machine's home directory. A pull request is now open for this work and will be merged at the start
of the next session unless the operator merges it earlier.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | block, PR body, Built State, round-10 booking, plan rewrite |
| C2 | done | rotation exit 0, both ledgers byte-equal to the prepared files |
| C3 | done | STATUS, README, self-use queue all byte-equal to the prepared files |
| Gate 1 | done | `verify.py` `ALL True` (C3 `absent` at gate time, expected) |
| Gate 2 | done | STATUS line occurs exactly once, no `- [~]` line |
| Gate 3 | done | exit 0, 859 passed, no FAILED/ERROR/SKIPPED |
| Gate 4 | done | integrity exit 0, `fail_count` 0 |
| Gate 5 | done | the eight open ids match exactly |
| Push | pending | runs once immediately after this commit |
| Pull request | pending | created immediately after the push; no number exists yet |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. The Open PR Gate, which merges F157's pull request in the NEXT session — never in this one.
3. The booking of round 11's verdict in the next feature's first commit.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`, currently F152 — Worker config
   isolation.

Operator questions open: 2.
Open findings: 8 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448 and R-1450, owned by
F316).
