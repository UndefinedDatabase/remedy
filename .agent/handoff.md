# Handback — F033 · SESSION 6 CLOSE · rounds 21 through 24

> Written by the REVIEWER at the close of session 6 and applied by a worker,
> because the reviewer writes no work-tree file itself. It carries the round 24
> verdict and the operator scope report. Operator amendment amend0827 rule 1: a
> verdict committed and pushed HERE is persisted, and is booked into
> `.agent/live_review.md` in the FIRST COMMITS of the next round that is
> happening anyway — never in a round of its own.

## Session

SESSION 6 of feature F033 · rounds 21, 22, 23 and 24 delegated · rounds so far 24.
The NEXT session is SESSION 7, which is the LAST under the amend0827 rule 6
soft limit of 7 sessions, and its first round would be round 25, which is the
other half of that limit. Both triggers arrive at once. See "Scope report".

## Fortschritt

~97 % (T001, T002 and T003 complete. The feature's FUNCTIONAL scope closed at
round 24: an operator's rejected hunks are recorded, selected, rebuilt and
quoted verbatim into the next builder prompt, proved through the real loop.
What remains is not feature work — the `docs/` obligation, the integration
gate, and the closure sequence) — Schätzung.

## Range

`98ce168e`..`a54f943e` on branch `feature/f033-hunk-approval-v2`, pushed;
`origin/feature/f033-hunk-approval-v2` is at the same commit. Session 6 added 33
commits. Every round was gated by the reviewer, which re-ran each round's own
gates from scripts of its own, reproduced every ordered reading, and re-ran
every mutation with its own anchors in its own disposable worktree before
writing a verdict.

## Verdicts

| Round | Subject | Verdict | Ledger entry |
|-------|---------|---------|--------------|
| 21 | rejected hunks as a builder-prompt steering segment | PASS | `Gate: F033 R21` at `61d2ffe7` |
| 22 | R-0747 repaired; the ledger export gains its inverse | PASS | `Gate: F033 R22` at `ce6c2866` |
| 23 | a stored decision reaches the real loop's prompt | PASS | `Gate: F033 R23` at `90af5927` |
| 24 | R-0748 repaired; the job-level wiring | PASS | NOT YET BOOKED — below |

## Round 24 verdict — PASS, and it is not yet in the ledger

The next round books it. Every gate was re-executed by the reviewer at
`a54f943e`. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r24.md`
against the reviewer's own pre-emission original was SILENT, as was the
comparison against `.agent/last_block.md`; the worker copied the file with
`shutil.copyfile` rather than retyping it. THE PAIR: PAIRDOC-FROM occurs 0 times
and PAIRDOC-TO exactly 1 time in the acceptance test file, and round 23's
superseding comment block is preserved untouched, as ordered. THE SWEEP, which
is R-0748's actual fix: `persists no decision` and `persists NOTHING` each occur
ZERO times across `packages/`, `apps/`, `tests/` and `docs/`, confirmed by the
reviewer in four independent forms — `git grep` over tracked content, a
source-only grep, and a broad grep that also reads binaries — all at REAL exit 1.
THE PROSE FILES: `.agent/plan.md` byte-EQUAL to PLAN24 at 46 lines;
`.agent/prose_slips.md` reconstructs 30807 plus one newline plus 529 to 31337.
THE RECORD APPEND at `90af5927` reconstructs 1595141 plus one newline plus 7458
to 1602600, base a byte PREFIX, slice an exact SUFFIX, N COUNTED at 2, and a
negative control at byte 1596121 — the reviewer's own offset, inside the FIRST
appended paragraph's span 1595142 to 1600036 — REJECTED by both readers, which
accepted the unflipped bytes. THE LEDGER: registered 308 to 309 with the ADDED
id exactly `R-0748`; `Done:` 53 lines over 51 distinct UNMOVED at all three
revisions; `Landed:` 19 to 20 with `^Landed: R-0748 — ` 0 before C4 and exactly
1 at it; `^Gate: F033 R23 — ` 0 before and exactly 1 after; and the open set 257
to 258. THE CODE: `python3 -m ruff check` exits 0 over all three changed files;
the helper is module-level; and the `run_pingpong` call passes
`hunk_ledger=_recorded_hunk_ledger_for_task(job, task)`. THE MUTATIONS were
re-run in the reviewer's own disposable worktree at C6 with its OWN anchors,
each asserted UNIQUE and the file restored and proved byte-identical by sha256:
control a REAL exit 0 at 10 passed; a fixed task id is exit 1 at 4 failed,
naming the different-task test and the job-scope boundary test; removing the
structural guard is exit 1 at exactly 2 failed, both attribute-access cases,
which shows the outer guard and the reader's own guard are measured by DISJOINT
tests; and removing the wiring is exit 1 at 1 failed. THE SUITES were re-run
SERIALLY in the primary checkout, every REAL exit 0: the five orchestration
suites 274 together, and the canary 42. THE STRUCTURE: nine single-parent
commits over `c9dd471f`..`a54f943e` of 334, 262, 22, 4, 2, 11, 49, 241 and 262
insertions, every one under 500, the last being the handback commit no gate of
the block could reach; and the path set to C6 EQUALS the declared change set in
BOTH directions.

## The two deviations that were worth more than the gates

D1 — G5 WENT RED ON ITS FIRST RUN AND THE WORKER WAS RIGHT ABOUT WHY. A broad
`grep` matched a stale gitignored `__pycache__` `.pyc` compiled from the
pre-repair source, while `git grep` over tracked content was already clean. The
worker removed that ONE file BY EXACT PATH as build-artifact hygiene, re-ran the
gate UNMODIFIED, and re-ran it again after the suites regenerated bytecode. The
fault is the REVIEWER'S GATE, not the repository: a sweep worded "occurs 0 times
across these trees" and run with a plain recursive grep reads compiled
artifacts, so it can be red while the source property holds and green while it
does not. The counter-measure is to sweep TRACKED CONTENT. Nothing on disk was
wrong, so under amend0827 rule 2 this spends no id.

D2 — THE WORKER CAUGHT THAT ITS MUTATION GATE COULD HAVE BEEN VACUOUS, and the
question reaches back across this whole session. `/home/decodeux/Repos/remedy`
is on `sys.path` through a `.pth`, so a worktree run could import the PRIMARY
checkout's copy and every mutation would then be a no-op that still reports a
pass. The worker built a runner pinning the worktree at `sys.path[0]` and
printing the resolved `__file__`. THE REVIEWER SETTLED IT RATHER THAN ACCEPTING
IT: measured at `5cb87f37`, under `cwd=<worktree>` both a plain script run and a
pytest run resolve `packages.orchestration.pingpong_job` to the WORKTREE's copy,
because the working directory precedes the `.pth` entry. The mutation proofs of
rounds 21 through 24 were therefore NOT vacuous, and the reds corroborate it
independently — a vacuous run cannot go red at all, and every ordered mutation
went red naming the expected tests. The reviewer's own round 24 mutation run
additionally asserted `.remedy-wt/rv-r24` inside the module's `__file__` before
mutating anything, so the claim is now measured rather than inferred.

## What this session built

| Path | What it decides | Round |
|------|-----------------|-------|
| `packages/orchestration/pingpong_loop.py` | the `builder_hunk_rejections` steering segment, and the loop's forwarded ledger | 21, 23 |
| `packages/orchestration/hunk_ledger.py` | `import_hunk_ledger`, the inverse of the export | 22 |
| `packages/orchestration/hunk_decision_record.py` | `load_latest_hunk_ledger_from_metadata`, the read side | 23 |
| `packages/orchestration/pingpong_job.py` | the last hop: the job's recorded decision reaches the loop | 24 |

R-0747 was raised and RESOLVED; R-0748 was raised and its fix LANDED, awaiting
the reviewer's resolution at the next gate. The open set went 257 to 258.

## SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

## Scope report — required by operator amendment amend0827 rule 6

WHY IT IS OWED NOW. The soft limit is 25 ROUNDS or 7 SESSIONS, whichever comes
first. This feature stands at 24 rounds and 6 sessions, so session 7 reaches
BOTH at once: it is the seventh session and its first round is the
twenty-fifth. The report is written here, one round early, so session 7 opens
with it instead of spending a round producing it.

WHAT IS FINISHED. The feature's Goal & Done is met on every clause the feature
file states. Stable content-hash ids with their stability property (T001).
The command, its validation, all-or-nothing subset apply, the hunk ledger and
the write door (T002). Partial-state truth on all three surfaces — viewer, task
node and report line (T003, R-0738). And the rejection-to-repair loop, complete
end to end as of round 24: an operator's rejection is recorded on the job,
selected back out by task, rebuilt into a ledger, rendered as repair findings
with the reason held byte for byte, and composed into the next builder prompt —
proved by driving the real loop and matching the composed segment's digest.

WHAT IS MISSING, and none of it is feature work:
  1. `docs/` owes an operator-facing description of `remedy patch approve-hunks`.
     No round has been allowed a `docs/` path in this whole feature, so this is
     a first — one round, and it carries the `tests/docs/` gate the docs-round
     rule adds.
  2. The integration-gate round, per docs/agents/integration_gate.md.
  3. The closure sequence and its pull request, which by precedent on this
     branch is two rounds.
  4. R-0745 (Low, OPEN) — the write door's import guard reads DIRECT imports
     only, and the door's transitive closure now reaches `subprocess` through
     `evidence_index`. Its fix clause names two routes and recommends the
     transitive-closure test.

That is four to five rounds against the one the limit leaves.

THE PROPOSAL, and it is a proposal only. SPLIT R-0745 OFF ONTO ITS OWN STATUS
LINE and let F033 close on the Acceptance it has met. The reasoning: R-0745 is
not part of F033's Goal & Done, is not reachable from any clause of its
Acceptance, and was raised opportunistically by the reviewer at the R15 gate
from a measurement no gate ordered. It is a hardening of a guard that protects
the HTTP door — genuinely worth doing, and genuinely not this feature. Carrying
it blocks a feature that is otherwise complete, and a Low finding blocking a
finished feature is how a roadmap stops meaning anything. Items 1 through 3
above are closure obligations proper and stay with F033; on that split, session
7 closes the feature in three to four rounds, which fits if the operator accepts
one round over the soft limit or grants an eighth session.

THE ALTERNATIVE, recorded because rule 6 asks for one: keep R-0745 inside F033
and expect an eighth session. This is the safer reading of "a feature closes
with its findings resolved", and the reviewer does not recommend it only because
the finding is Low, is not about this feature's behaviour, and has a fix whose
better half — the transitive-closure test — is a guard-hardening task that
deserves its own round rather than a corner of a closure round.

NEITHER OPTION IS EXECUTED ON THE REVIEWER'S OWN AUTHORITY. Session 7 proceeds
on the recommended option unless the operator says otherwise, and records
whichever it takes as a DECISION with its reversal.

## Next expected action — SESSION 7, in this order

1. Read `.agent/STOP` from disk. If it exists, hand off and end — Phase 1 rule 1
   before rule 2, finding R-0347.
2. Run the Open PR Gate. There was no open PR at the close of session 6 and this
   session created none.
3. READ THE SCOPE REPORT ABOVE BEFORE PLANNING ANY WORK. The soft limit is
   reached at this session's first round.
4. That round's FIRST commits book, into `.agent/live_review.md`, the round 24
   verdict above and the authored `Done: R-0748` resolution. Neither buys a
   round of its own.
5. Then the `docs/` round: the operator-facing description of
   `remedy patch approve-hunks`. Its gate adds `python3 -m pytest tests/docs/ -q`
   to the canary, per the docs-round rule, and a ledger-count change and its
   test pin must land in the SAME commit.
6. Then the integration gate, then closure.
7. A standing lesson from this session, for whoever writes the next gates: a
   sweep asserting a string is absent must search TRACKED CONTENT, because a
   plain recursive grep also reads gitignored build artifacts; and a gate whose
   fix clause names ONE FILE while the defect is a CLAIM will leave that claim
   standing everywhere else, which is exactly how R-0747 became R-0748.
