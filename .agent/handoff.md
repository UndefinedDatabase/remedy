# Handback — F157 "Capability matrix & honest degradation," round 1

## Session

SESSION 1 of feature F157 · round 1 · rounds so far 1

Context self-assessment: this session verified `digests.txt`'s own sha256 and every prepared
file's sha256 before using any of them, applied C1's six byte copies with a direct equality check
per file, found that C2 (`.agent/f157_inventory.md`, 309 lines) was already landed on this branch
by a concurrent process sharing this checkout — verified its content against the block's seven
required sections and adopted it as-is rather than duplicate it — ran all four gates fresh to the
exact readings the block requires, and is about to commit C3 with this handback and push, with no
pull request opened by this round.

State block:
Feature F157 (claimed `[~]`), branch `feature/f157-capability-matrix`, base `0f811a713`.
Fortschritt: ~15 % (T001 inventory landed · T002 and T003 open) — Schätzung

## Range

Review of `0f811a713`..HEAD.

## Commits

### 47ceff49d F157 R1 C1: claim F157, book F314 R9, re-head the ledger, DECISION F157 D1
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f157-r1.md` | +129/-0 | NEW FILE; byte copy of the reviewer-authored block, `block.md` |
| `.agent/context.md` | +10/-8 | rewritten for F157 round 1 |
| `.agent/decisions.md` | +10/-0 | DECISION F157 D1 appended |
| `.agent/live_review.md` | +22/-20 | re-headed at the F157 claim; F314 round 9's verdict booked at the end |
| `.agent/plan.md` | +15/-10 | rewritten for F157 round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F157's line `[ ]` → `[~]` |

All six paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py` and a
direct byte-equality check (this session's own, independent of C2's author) confirm each equality.

### fbde31b6d F157 R1 C2: T001, the inventory of every capability check, its fallback and its tests
| Path | +/- | Reason |
|---|---|---|
| `.agent/f157_inventory.md` | +309/-0 | NEW FILE; T001's findings-pass inventory, written from reading the code at `0f811a713`, under 400 lines, read-only (no other file touched); reviewed before any code is authored |

This commit was made by a concurrent process that was independently executing this same round's
block on this same shared checkout (see Deviations). This session read the resulting file in
full, confirmed it carries no machine path, is 309 lines, follows the block's seven required
sections in order with a `path:line` on every factual sentence, and that the diff touches only the
one named path — then adopted it rather than writing and committing a competing version of the
same deliverable.

### this commit — F157 R1 C3: handback
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | n/a (self-reference; R-0149 pattern) | this handback, rewritten per `docs/agents/handback_template.md` |

## Item status

| Item | Status | Reason |
|---|---|---|
| C0 | done | branch `feature/f157-capability-matrix` created from `main` at `0f811a713` |
| C1 | done | `47ceff49d`, exactly the six named paths, each byte-equal to its prepared `c1-*` file |
| C2 | done | `fbde31b6d`, exactly `.agent/f157_inventory.md`, 309 lines, no machine path; made by a concurrent process on the same checkout, verified and adopted by this session (see Deviations) |
| C3 | done | this commit, the handback alone |
| Gate 1 (`verify.py`) | done | every line `True`, `C3` read `absent` before this commit, last line `ALL True` |
| Gate 2 (pytest selection) | done | exit 0, `3765 passed, 2 skipped`, no FAILED/ERROR line, no `process(es) behind` line |
| Gate 3 (integrity) | done | `fail_count` 0, all 6 checks pass |
| Gate 4 (open ids) | done | count `8` |
| Push | pending | ordered to run immediately after this commit; see this session's reply for the result |

## External actions

No push, `gh` command or worktree action has run yet at the moment this file is written: the
block orders the push to follow this commit, and no pull request is opened by this round. Its
outcome is reported in this session's final reply, not rewritten into this file (write-once rule,
PH v3).

Three `SendMessage` calls went to the concurrent subagent sharing this checkout
(`a1b2341d9e3daa718`): first asking it to stop, then correcting that to "proceed, I'll stand down"
on seeing its near-complete, correct state, then a final message after roughly nine minutes with
no further repo activity from it, saying this session was taking over C3 and the push and asking
it to take no further action on this branch. No reply was received from it by the time this file
is written.

One scratch directory used, `.remedy-wt/f157-r1-worker/` (created this round), holding the
digest-verification script, the C1 copy-and-verify script, and this session's own independent gate
runs. `.remedy-wt/f157-r1/` (the reviewer's prepared tree) was only read, never written.

## Verification

Gate order per the block, run once each by this session after adopting C2's already-committed file
and before this commit — independent of whatever gate run the concurrent process may have made.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f157-r1/prep/verify.py .` → every line `True` (`C3` read `absent`), last
   line `ALL True`. Full output:
   ```
   True	47ceff49d single parent equal to the commit before it
   True	47ceff49d insertions 187 under 500
   True	fbde31b6d single parent equal to the commit before it
   True	fbde31b6d insertions 309 under 500
   True	every commit carries a F157 R1 Cn subject: 2 of 2
   True	on feature/f157-capability-matrix
   True	C1 paths exactly [...]: [...]
   True	C1 .agent/authored/f157-r1.md equals c1-.agent__authored__f157-r1.md
   True	C1 .agent/context.md equals c1-.agent__context.md
   True	C1 .agent/decisions.md equals c1-.agent__decisions.md
   True	C1 .agent/live_review.md equals c1-.agent__live_review.md
   True	C1 .agent/plan.md equals c1-.agent__plan.md
   True	C1 docs/roadmap/STATUS.md equals c1-docs__roadmap__STATUS.md
   True	C2 paths exactly ['.agent/f157_inventory.md']: ['.agent/f157_inventory.md']
   True	C2 .agent/f157_inventory.md holds no machine path
   True	C2 .agent/f157_inventory.md has 309 lines, under 400
   absent	C3
   True	the saved block equals block.md
   ALL True
   ```

2. `python3 .remedy-wt/f157-r1/prep/run_selection.py . .remedy-wt/f157-r1-worker/selection-output.txt`,
   run once:
   ```
   paths 82
   exit 0
   3765 passed, 2 skipped in 28.37s
   SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
   SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
   ```
   `exit 0`, no `FAILED`, `ERROR` or `process(es) behind` line.

3. `python3 -m apps.cli.main integrity check --json`, run once:
   ```
   {"check_count": 6, "checks": [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
   ```
   `fail_count` 0, all six checks `pass`.

4. `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"`
   → `8`, the exact count required.

## Authored-text proofs

- `digests.txt` was checked against its own stated sha256
  (`86e7fbf0436b49c8e6c1e90f9632fe4f6f920601b66702e04ca1789b3eb5c51e`, matched), then every one of
  its ten listed entries was checked with a Python sha256 reader and every one read `OK` — all
  before any prepared file was copied, run or read.
- `.agent/authored/f157-r1.md` against `block.md`: identical sha256
  (`c9a8604c0901a5075a19ff6709f4d2415d6865bcefe2fe95ca35eac7b0b2b7d4`) and identical `wc -l` (129
  both). Byte-identical.
- All six C1 paths proved byte-identical to their `c1-*` prepared files with a direct read-only
  comparison script before staging, and confirmed again by gate 1's `verify.py` after the commit.
- `.agent/f157_inventory.md` (C2) is a findings-pass write (T001), not reviewer-authored text; no
  authored-text proof applies to it. This session additionally confirmed it independently against
  the block's own requirements (seven sections in order, `path:line` on every factual sentence, no
  machine path, 309 lines, diff touching only the one named path) before adopting it as the
  round's C2, since it was not this session's own writing.

## Deviations & assumptions

**Concurrent worker on the same checkout (the one deviation this round).** This session found,
partway through its own work, that a second agent process (`a1b2341d9e3daa718`, visible via
`ListAgents` as a subagent of this same top-level session) was independently executing this exact
block on this exact shared primary checkout at the same time. This session's own C1 (`47ceff49d`)
had already landed before the collision was noticed; the other process then committed `fbde31b6d`
(C2) nine minutes later and began writing (but never committed) its own `.agent/handoff.md` for
C3. This session sent it a stop message, then a correction asking it to proceed since it was
further along and its work was correct, then, after roughly nine minutes with no further file
changes and `ListAgents` still showing it as "running," a final message announcing this session
was taking over C3 and the push. No reply was ever received from it. This session independently
verified C2's content against the block before adopting it (see Authored-text proofs), discarded
the other process's in-progress, uncommitted `.agent/handoff.md` draft (`git checkout --
.agent/handoff.md`), and re-ran every gate itself rather than trusting the other process's gate
output. No commit, path, or gate reading in this handback is taken on trust from the other
process: C1 is this session's own, and C2's CONTENT was independently checked line-by-line against
the block's requirements even though this session did not author it. Beyond this collision, C1 and
C2 landed in the block's exact order, on the one branch, with no extra, dropped or reordered
commit; all four gates read exactly what the block required.

## For the operator, in plain sentences

This session claimed a new piece of work about how Remedy's workers tell the truth about what a
model can and cannot do, instead of a feature silently assuming it. It wrote down, in one
reviewed document, every place in the program today that already guesses or hard-codes an answer
to that question, and every place that has no answer at all yet. It found that one capability the
program already declares is never actually read by a running job, that a job's own chat badge no
longer has a home to live in because the old web page was removed last week, and that a few
useful words this work wants to reuse already mean something else in the program, which the next
piece of work will need to pick around. Partway through, this session discovered that another copy
of itself was doing the very same work on the very same checkout at the same time; it talked to
that other copy, decided the other copy's inventory document was correct, kept it instead of
writing a second one, and finished the round on its own once the other copy stopped responding.
Nothing in the running program changed this session; only the written record of what exists did.
The next session designs and builds the actual module from what this session found.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else. `.agent/STOP` does not exist at
   the time this file is written.
2. Rule 2, the Open PR Gate: this branch carries no pull request yet, so the next session's gate
   finds none open for it and continues normally.
3. The booking of this round's verdict happens in the next round's first commit.
4. T002: the matrix module and its guards, framed by DECISION F157 D2 from this round's reviewed
   inventory.

Operator questions open: 2. Open findings: 8.
