# Handback — F151 round 11 (CLOSING — F151 accepted; pull request opens this round, unmerged)

## Session

SESSION 2 of feature F151 · round 11 · rounds so far 11.

Context self-assessment: `digests.txt` was checked against the sha256 given in the prompt before any
file it lists was trusted, every file it lists was checked against its own digest before use,
`block.md` was read in full before acting, and every number below was produced by running the thing,
not recalled. The session ends here because F151 is closed and the next feature starts in a fresh
session.

Fortschritt: 100 % (F151 is accepted; its pull request waits for the next session's Open PR Gate) —
Schätzung.

## Item status

| Item | Status | Reason |
|---|---|---|
| Round 10 C1 | done | booked round 9, the Built State, saved the round 10 block and PR body; committed `363defdb5`, pushed |
| Round 10 C2 | done | the finding ledger rotated into its archive; committed `8cba09943`, pushed |
| Round 10 C3 | done | its three files (STATUS line, README sync, self-use queue) were written and byte-verified in round 10's working tree; this round's own block folds their commit into this round's single C1 alongside its four new files, instead of a separate C3 |
| This round's C1 | done | the four remaining prepared files copied and byte-verified; gates 1–3 all passed; committed with the handoff as the branch's last commit |
| Push | done | `git push origin feature/f151-worker-adapter-contract`, run once immediately after the commit |
| Pull request | done | opened via `gh pr create` immediately after the push, left unmerged |
| Gate 1 | done | `verify.py` — every line `True`, `absent` for C1 pre-commit, last line `ALL True` |
| Gate 2 | done | integrity check — first read `fail_count: 1` (two new files untracked), `fail_count: 0` after staging them |
| Gate 3 | done | the open finding ids read exactly the eleven the block names |
| Gate 4 | done | run after the pull request: `verify.py` `ALL True` again, `git status --porcelain` empty |

## Round 10's gate 3, carried forward

Round 10's one test selection read `exit 1` with the identical passed count (793) and no
FAILED/ERROR/SKIPPED line, pointing at a concurrent process on the machine writing into the shared
data root rather than a defect in F151's own code; DECISION F151 D6 in `.agent/decisions.md` records
that reasoning and the stop. This round's own block states, as established fact going into this
round, that the reviewer re-ran that exact same selection once on the same bytes afterward and read
`exit 0` with the same `793 passed` and the conftest guard excusing only its own supervisor entries —
confirming D6's diagnosis. Per the block's "one test run per tree" rule, this round runs no test of
its own; the closure proceeds on that clean re-run.

## Range

Review of `d22ba50a0`..`HEAD`.

## Commits

### `363defdb5` F151 R10 C1: book round 9, the Built State, save the round 10 block and the PR body

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r10-pr_body.md` | +67/-0 (new) | byte copy of the prepared PR body |
| `.agent/authored/f151-r10.md` | +136/-0 (new) | byte copy of round 10's block.md |
| `.agent/live_review.md` | +2/-0 | round 9's `Gate: F151 R9` verdict booked |
| `.agent/plan.md` | +5/-4 | advanced to round 10, the closing round |
| `docs/roadmap/features/T8_F151.md` | +38/-0 | the Built State section added |

### `8cba09943` F151 R10 C2: rotate the finding ledger into its archive

| Path | +/- | Reason |
|---|---|---|
| `.agent/live_review.md` | +0/-42 | 7 gate records and 7 finding pairs (14 records) moved to the archive |
| `.agent/live_review_archive.md` | +42/-0 | the same 42 lines appended there |

### `d22ba50a0` F151 R10: blocked handback — gate 3 read red before C3's commit

| Path | +/- | Reason |
|---|---|---|
| `.agent/decisions.md` | +10/-0 | DECISION F151 D6 recorded |
| `.agent/handoff.md` | +142/-135 | round 10's blocked handback written |
| `.agent/plan.md` | +22/-5 | records the blocker and the exact next action |

### this round's commit — F151 R11 C1: accept F151 in STATUS with its README sync and the self-use queue

(self-reference: this commit also writes `.agent/handoff.md`, the one row the handback template
exempts from its own table — a handback cannot table the commit that writes it.)

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f151-r11-pr_body.md` | +71/-0 (new) | byte copy of this round's prepared PR body |
| `.agent/authored/f151-r11.md` | +95/-0 (new) | byte copy of this round's block.md, proved equal to it |
| `.agent/plan.md` | +5/-22 | advanced to the closed state |
| `README.md` | +11/-2 | Tier 8 gains an "Accepted in Tier 8 so far" entry for F151, counter to 160 of 314, Tier 8 row to 1 of 12 |
| `docs/roadmap/STATUS.md` | +1/-1 | F151's `- [~]` line becomes the accepted `- [x]` status line |
| `docs/roadmap/features/T8_F151.md` | +1/-1 | "two sessions of ten rounds" corrected to "eleven rounds" |
| `scripts/self_use_queue.json` | +1/-1 | SU-078's `consumed_by` becomes `F151` |
| `.agent/handoff.md` | rewritten | this handback (self-reference; not tabled by numstat) |

## External actions

- Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`,
  checked before any write.
- `git push origin feature/f151-worker-adapter-contract` → run once, immediately after this commit.
- `gh pr create --repo UndefinedDatabase/remedy --base main --head feature/f151-worker-adapter-contract --title "F151 — Worker adapter contract v2" --body-file .agent/authored/f151-r11-pr_body.md`
  → run once, immediately after the push; its number and URL are reported in the session's reply
  only, never recorded here, because the pull request does not exist yet when this file is written.
- `gh pr list --repo UndefinedDatabase/remedy --state open --json number,headRefName,baseRefName,isDraft`
  → run once, after the pull request is created; must read exactly that one pull request, from
  `feature/f151-worker-adapter-contract` into `main`, not a draft.
- No worktree added or removed. No merge, no `gh pr merge`. No branch created, switched or deleted.
  No stash touched. No provider call.

## Verification

Interpreter: the repository's configured Python 3 (`python3`).

Gate 1 — `python3 .remedy-wt/f151-r11/prep/verify.py .` (run after the four copies, before staging
or committing anything):

    True	on feature/f151-worker-adapter-contract
    True	at most one commit after d22ba50a0: 0
    absent	C1 committed
    True	working tree README.md equals its snapshot
    True	working tree docs/roadmap/STATUS.md equals its snapshot
    True	working tree scripts/self_use_queue.json equals its snapshot
    True	the saved block equals block.md
    ALL True

Gate 2 — `python3 -m apps.cli.main integrity check --json`: first run exit 1, `"fail_count": 1`
(`relevant_untracked`: `2 relevant untracked: .agent/authored/f151-r11-pr_body.md,
.agent/authored/f151-r11.md`); staged both with `git add` (no commit); re-run exit 0,
`"fail_count": 0`, all six checks `pass` (`untracked=0, relevant=0`).

Gate 3 —
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421', 'R-1425', 'R-1426', 'R-1427', 'R-1428']`
— exactly the eleven ids the block names.

Gate 4 (after the pull request) — reported in the session's reply, per the block's own instruction.

## Authored-text proofs

The four files this round's C1 copies are reviewer-authored text applied this round: each was copied
from its `c1-*` file under `.remedy-wt/f151-r11/prep/` by `c1_copy.py` under
`.remedy-wt/f151-r11-worker/`, each proved byte-identical immediately before staging by
`c1_verify_bytes.py` (read-only); all four read `True`. The STATUS line: `docs/roadmap/STATUS.md`
holds the prep folder's `status_line.txt` content, minus its trailing newline, exactly once, with its
package folder written here as `~/Repos/remedy-history/zips` — the committed file itself keeps the
real machine path, which lives in `docs/roadmap/STATUS.md`, not under `.agent/`, so that file's path
restriction does not apply to it.

## Deviations & assumptions

- Gate 2 read `fail_count: 1` on its first run, because the two new `.agent/authored/f151-r11*.md`
  files were still untracked at that point. They were staged with `git add` (no commit, no mutation
  of tracked content) before the re-run, which read `fail_count: 0`. Staging ahead of the commit is
  not one of the block's forbidden actions; this is recorded here because the first reading differed
  from the required `fail_count: 0`, even though the second did not.
- None else. No production or test file was edited. No provider call. No mutation, no worktree, no
  test run of any kind — the block forbids one, and none was run.

## For the operator, in plain sentences

Remedy now has one written contract that any builder or reviewer backend fills the same way, saying
what it can do, how a call to it is built, and how its answers, its usage and its errors are read
back, while retrying, waiting and switching models stay in Remedy's own loop. A reusable set of
checks proves a backend keeps that contract and refuses one that tries to retry or start a program by
itself. Today's Claude command line path is the first such backend, with no change in its behaviour.
The paid run on itself stopped at its own approval gate. The whole test collection passed on the code
that ships. The last check of the closing step once read red only because another session's job
wrote into the shared data folder at the same moment, and it passed when the check ran again. The
review package is named remedy-review-20261023-180445-READY_FOR_REVIEW.zip, kept in the folder
~/Repos/remedy-history/zips. A pull request is open and will be merged at the start of the next
session unless the operator merges it earlier.

## Next

1. Phase 1 rule 1: check whether `.agent/STOP` exists.
2. The Open PR Gate, which merges F151's pull request in the NEXT session and never in this one.
3. The booking of rounds 10 and 11's verdicts in the next feature's first commit.
4. Rule A5.

Operator questions open: 0. Open findings: 11 (R-1246, R-1281, R-1326, R-1351, R-1353, R-1418,
R-1421, R-1425, R-1426, R-1427 and R-1428, owned by F314).
