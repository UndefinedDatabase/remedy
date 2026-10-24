# Handoff — F152 round 10 (the closing round)

## Session

SESSION 1 of feature F152 · round 10 · rounds so far 10. This session verified every prepared
digest before touching a file, applied the three byte copies and the one ledger rotation exactly,
found all five gates green, and wrote this handback with no finding of consequence. The session
ends here because F152 is closed and the next feature starts in a fresh session.

Fortschritt: 100 % (F152 is accepted; its pull request waits for the next session's Open PR Gate) —
Schätzung.

## Range

Review of `451ab8807`..`139945b2c` (C1 to C2; C3 — this file — is the commit that carries it, per
the handback template's self-reference exception).

## Commits

### 901425b14 F152 R10 C1: book round 9 and R-1464, the Built State, save the round 10 block and the PR body
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f152-r10-pr_body.md` | +78/-0 | NEW FILE — the pull request body, byte-copied from the prepared `c1-` file |
| `.agent/authored/f152-r10.md` | +144/-0 | NEW FILE — this round's block, the authored-text proof, byte-copied from the prepared `c1-` file |
| `.agent/live_review.md` | +4/-0 | round 9's PASS verdict booked as a Gate entry; R-1464 raised (the real-binary A/B), owned by F316 |
| `.agent/plan.md` | +5/-8 | rewritten: Current Step/Next Steps to round 10's closure |
| `docs/roadmap/features/T2_F316.md` | +4/-0 | F316's Acceptance line for R-1464 (amend0911-feedback rule A) |
| `docs/roadmap/features/T8_F152.md` | +48/-0 | F152's Built State |

### 139945b2c F152 R10 C2: rotate the finding ledger into its archive
| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-68 | rotated: resolved records and closed gate/finding pairs moved out |
| `.agent/live_review_archive.md` | +68/-0 | rotated: the same 68 lines appended to the archive |

### (this commit) F152 R10 C3: accept F152 in STATUS with its README sync and the self-use queue
| Path | +/- | Reason |
|---|---|---|
| `docs/roadmap/STATUS.md` | +1/-1 | F152's `[~]` line becomes its accepted `[x]` line |
| `README.md` | +9/-2 | `164 of 316`; Tier 8 row `4 \| 13`; Tier 8 list gains F152's entry after F157's |
| `scripts/self_use_queue.json` | +1/-1 | `SU-082`'s `consumed_by` becomes `F152` |
| `.agent/handoff.md` | rewritten | this file — carried alone, per the handback template's self-reference exception (R-0149) |

## External actions

`gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`, checked before any
write. No pull request created, edited or merged yet — this commit is written before the push, per
the block's ordering ("Name no pull request number: it does not exist when the handoff is
written"). No `git worktree` command run by me. No stash entry touched. No `claude` binary invoked
by me; no provider call this round. `git push origin feature/f152-worker-config-isolation` and
`gh pr create` both run once, immediately after this commit, per the block's THEN section; their
real outcomes are reported in the session reply, not in this file.

## Verification

**Gate 1.** After C3's three files were copied and staged: `git status --porcelain` →
```
M  README.md
M  docs/roadmap/STATUS.md
M  scripts/self_use_queue.json
```
only the three C3 files (exit 0). Then `python3 .remedy-wt/f152-r10/prep/verify.py .` (the
repository root):

```
True	901425b14 single parent equal to the commit before it
True	139945b2c single parent equal to the commit before it
True	every commit carries a F152 R10 Cn subject: 2 of 2
True	on feature/f152-worker-config-isolation
True	C1 paths exactly the manifest's: ['.agent/authored/f152-r10-pr_body.md', '.agent/authored/f152-r10.md', '.agent/live_review.md', '.agent/plan.md', 'docs/roadmap/features/T2_F316.md', 'docs/roadmap/features/T8_F152.md']
True	C1 .agent/authored/f152-r10-pr_body.md numstat 78 0 equals 78 0
True	C1 .agent/authored/f152-r10-pr_body.md equals c1-.agent__authored__f152-r10-pr_body.md
True	C1 .agent/authored/f152-r10.md numstat 144 0 equals 144 0
True	C1 .agent/authored/f152-r10.md equals c1-.agent__authored__f152-r10.md
True	C1 .agent/live_review.md numstat 4 0 equals 4 0
True	C1 .agent/live_review.md equals c1-.agent__live_review.md
True	C1 .agent/plan.md numstat 5 8 equals 5 8
True	C1 .agent/plan.md equals c1-.agent__plan.md
True	C1 docs/roadmap/features/T2_F316.md numstat 4 0 equals 4 0
True	C1 docs/roadmap/features/T2_F316.md equals c1-docs__roadmap__features__T2_F316.md
True	C1 docs/roadmap/features/T8_F152.md numstat 48 0 equals 48 0
True	C1 docs/roadmap/features/T8_F152.md equals c1-docs__roadmap__features__T8_F152.md
True	C2 paths exactly the manifest's: ['.agent/live_review.md', '.agent/live_review_archive.md']
True	C2 .agent/live_review.md numstat 0 68 equals 0 68
True	C2 .agent/live_review.md equals c2-.agent__live_review.md
True	C2 .agent/live_review_archive.md numstat 68 0 equals 68 0
True	C2 .agent/live_review_archive.md equals c2-.agent__live_review_archive.md
absent	C3 committed
True	C3 working tree README.md equals c3-README.md
True	C3 working tree docs/roadmap/STATUS.md equals c3-docs__roadmap__STATUS.md
True	C3 working tree scripts/self_use_queue.json equals c3-scripts__self_use_queue.json
ALL True
```
Every line `True` (C3 correctly `absent`, since C3 had not yet committed when this gate ran); the
last line `ALL True`.

**Gate 2.** The content of `status_line.txt` without its trailing newline occurs exactly once in
`docs/roadmap/STATUS.md`, and no line of it begins `- [~]`:
```
occurrences of status_line (no trailing nl) in STATUS.md: 1
lines starting with '- [~]': 0
GATE2 PASS
```

**Gate 3.** `python3 .remedy-wt/f152-r10/prep/gate3.py .` from the primary checkout, run once:
```
exit 0
953 passed in 93.17s (0:01:33)
NOTICE R-1411: 3 entries of the configured data root ~/Repos/remedy/.data changed in
the folders a supervisor this run did not start and its clients write; not counted (truncated to
300 chars by the script; the data root's path is this machine's and is written as `~` here).
integrity exit 0 6 pass; fail_count 0
```
`exit 0`, `953 passed` — the same passed count `sim-gate3.txt` reads (seconds differ, as permitted);
no `FAILED`, `ERROR` or `SKIPPED` line. A `NOTICE` line naming the data root did print, but DECISION
F151 D6's rerun exception applies only when gate 3 exits 1 with that notice; here gate 3 exited 0,
so no rerun was needed or performed.

**Gate 4.** Gate 3's integrity line: `integrity exit 0`, `"fail_count": 0`, all six checks `pass` —
matching `sim-gate3.txt`.

**Gate 5.** `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`,
run through a `cwd`-set Python subprocess wrapper (see Deviations for the one non-compliant first
attempt this replaces):
```
exit 0
['R-1246', 'R-1281', 'R-1351', 'R-1353', 'R-1426', 'R-1428', 'R-1448', 'R-1450', 'R-1464']
```
Exactly the nine ids the block names.

`git status --porcelain` after staging C3 (before this commit) showed only the three C3 files
modified, matching Gate 1.

## Authored-text proofs

C1's byte copy (`.remedy-wt/f152-r10-worker/c1_copy.py`, proved read-only by
`.remedy-wt/f152-r10-worker/c1_prove.py`) read `True` for all six targets immediately after
copying. C2's rotation (`.remedy-wt/f152-r10-worker/c2_rotate.py`) produced ledger files proved
byte-equal to the prepared `c2-` files by `.remedy-wt/f152-r10-worker/c2_prove.py`. C3's byte copy
(`.remedy-wt/f152-r10-worker/c3_copy.py`, proved by `.remedy-wt/f152-r10-worker/c3_prove.py`) read
`True` for all three targets. Gate 1's `verify.py` run independently re-confirmed every `C1 ...
equals c1-...` and `C2 ... equals c2-...` line `True`, and every `C3 working tree ... equals c3-...`
line `True`.

The STATUS line, the mandated proof: `docs/roadmap/STATUS.md` now holds, byte-identical to the prep
folder's `status_line.txt` without its trailing newline (occurring exactly once, per Gate 2):
`- [x] F152 — Worker config isolation (T001–T003 complete; accepted 2026-10-24 · live review
PASS_WITH_RISKS — ACCEPTED · Evidence job f152r9e1001 · package
remedy-review-20261024-111421-READY_FOR_REVIEW.zip · SHA-256
47ab419b8fe89aa50ff6106679c1089930649a4a1bebccfe6af6e6324dd30319 · package path
~/Repos/remedy-history/zips · accepted HEAD ab327e93f84f62018230713a4a8e46927e03567b)` (package
folder written as `~`, per the block's instruction).

The rotation's output, whole, from `.remedy-wt/f152-r10-worker/c2_rotate.py`:
```
exit 0
gate records moved: 11
finding pairs moved: 9 (18 records)
resolved-text records moved: 5
old ledger size: 171468 bytes
new ledger size: 142813 bytes
old archive size: 7345448 bytes
new archive size: 7374103 bytes
open findings before: 9
open findings after: 9
gate headers matching neither known form (left in place): 1
written: ~/.agent/live_review.md and ~/.agent/live_review_archive.md
```
The ledger's size: 171468 bytes before, 142813 bytes after; the archive's size: 7345448 bytes
before, 7374103 bytes after. Every output line but the `written:` line equals `sim-rotation.txt`'s
lines after its first line; the `written:` line differs only in the absolute path, which is this
machine's path rather than the simulation's disposable worktree path, as the block permits.

## Deviations & assumptions

1. Gate 5's required `python3 -c` command was first run through a shell `cd` into the repository
   root before the command, which the block's constraint "Never `cd`, not even into a scratch folder
   or the repository root" forbids. This was caught before any commit or decision depended on it.
   Gate 5 was immediately re-run through a compliant `cwd`-set Python subprocess wrapper
   (`.remedy-wt/f152-r10-worker/gate5.py`), producing the identical result reported above. The
   reported Gate 5 reading is the compliant rerun; the non-compliant one was discarded and nothing
   was built on it.

No other departure from the block's ordered commit sequence: no split, no correction commit, no
file touched outside the paths named per commit, no second test command beyond Gate 3's one scoped
pytest run, no `REMEDY_TEST_MAX_WORKERS`, no `-n` of my own, no `claude` binary invoked by me, no
worktree of my own, no mutation beyond the three ordered byte copies and the one rotation-script
run, and no `gh pr merge`, `git checkout`/`git switch`, branch creation/move/deletion or force-push.

## For the operator, in plain sentences

A worker Remedy starts no longer picks up the operator's personal settings for the model's
command-line tool — things such as the operator's own settings file and the tool servers it
configures — and it no longer picks up most of the operator's shell settings either, while the
operator's own login to that tool keeps working exactly as before. Every kind of worker must now
say, in a written record, how it keeps those personal settings out of a run, and a check refuses to
accept a worker that does not say so. Each run notes how it kept those settings out. The worker
check command now checks this for every kind of worker, not just one. The paid run this feature made
on itself wrote the first tests for one of Remedy's untested modules; a reviewer checked and passed
that work, though it is being kept unapplied for now; that same run was also the first real run
using the command-line tool without the operator's personal settings attached, and the login still
worked. The full proof that this holds against the real command-line tool in every case still waits
for the operator's permission, which this round's open questions ask for, and that proof is carried
forward to the next clean-up round. The whole test collection passed on the code that is about to
ship. The review package already built for this feature, named
`remedy-review-20261024-111421-READY_FOR_REVIEW.zip`, is still sitting on disk in its own folder,
ready for a human to open. A pull request for this feature is now open, and it will be merged
automatically at the start of the next work session unless the operator merges it sooner.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | six files byte-equal to the prepared snapshots; numstat matched the manifest exactly |
| C2 | done | rotation exit 0, output matched `sim-rotation.txt`; both ledger files byte-equal to the prepared snapshots |
| C3 | done | three files byte-equal to the prepared snapshots; committed with this handoff |
| Gate 1 | done | every line `True`, last line `ALL True` |
| Gate 2 | done | STATUS line occurs exactly once; no `- [~]` line remains |
| Gate 3 | done | exit 0, 953 passed (matches `sim-gate3.txt`), no FAILED/ERROR/SKIPPED |
| Gate 4 | done | integrity exit 0, `fail_count` 0, all six checks pass |
| Gate 5 | done | open ids exactly the nine the block names (after discarding one non-compliant `cd` attempt) |
| Push | pending | runs immediately after this commit, per the block's THEN section; outcome reported in the reply |
| Pull request | pending | created immediately after the push, per the block's THEN section; number and URL reported in the reply |

## Next

1. Phase 1 rule 1: check `.agent/STOP` before any new work.
2. The Open PR Gate — merges F152's pull request in the NEXT session, never in this one.
3. The booking of round 10's verdict in the next feature's first commit.
4. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

Operator questions open: 3.
Open findings: 9 (R-1246, R-1281, R-1351, R-1353, R-1426, R-1428, R-1448, R-1450 and R-1464, owned by
F316).
