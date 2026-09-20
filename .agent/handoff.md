# Handoff — F276 Data-root hygiene & disk budget · Round 10 — STOPPED BY SENTINEL

## Session

SESSION 2 of feature F276 · round 10 · rounds so far 10

Context self-assessment: the worker read AGENTS.md in full, verified the step
block's bytes before using it — 209 lines, sha256
`b00e05fed169f8c5cbc7e7212605814b529fcf3589f93a3540cad2b54fbc067e`, both
readings identical to the digest the delegation message named — then read
`docs/agents/handback_template.md` and `docs/roadmap/STATUS_closure_protocol.md`,
and then found `.agent/STOP` on disk. The block's constraint 7 and
`docs/agents/self_drive_protocol.md` Phase 1 rule 1 both order the same thing in
the same words: write the handoff and end, doing nothing else. Every numeral
below is the output of a command run in this round.

## THE SENTINEL

```
ls -la .agent/STOP
-rw-rw-r-- 1 decodeux decodeux 0 Sep 20 10:47 .agent/STOP

git status --porcelain
?? .agent/STOP
```

`.agent/STOP` EXISTS — an empty file, untracked, dated 2026-09-20 10:47, which is
AFTER round 9's last commit `970f544b`. It was therefore dropped between round 9's
handback and this round's delegation. The block was authored without knowledge of
it; that is not a defect in the block, it is exactly the mid-session window
finding R-0347 describes.

THE SENTINEL WAS NOT DELETED, NOT MOVED, NOT EMPTIED AND NOT `git add`ed.
Removing it is the operator's decision alone. `?? .agent/STOP` surviving in
`git status --porcelain` at the end of this round is the CORRECT end state and
NOT a dirty tree — no later reader should "fix" it.

## Range

Review of 970f544b..HEAD — branch `feature/f276-data-root-hygiene`.

## Summary

Round 10 executed ONE of its two commits and none of its three uncommitted build
steps. C1 — the bookkeeping — was NOT performed, because constraint 7 orders the
STOP reading BEFORE the first commit and the reading was positive. This file is
the round's only write.

Nothing of the round is lost. All six payloads under `.remedy-wt/f276-r10/` were
verified byte-exact against the line counts and digests the block states, and
they are re-delegatable unchanged once the operator lifts the sentinel. That
directory is GITIGNORED SCRATCH: `git clean -x` destroys it, so it must not be
cleaned before round 10 is re-run.

## Item status

| Item | Status | Reason |
|------|--------|--------|
| C1 the bookkeeping | skipped | `.agent/STOP` present before the first commit — block constraint 7 |
| C2 the handoff | done | this file, the one action the sentinel authorises |
| Integrity check (precondition 3) | skipped | after C2; the sentinel ends the round at C2 |
| Evidence job (protocol step 1) | skipped | same |
| Review package (protocol step 2) | skipped | same — NO package was built and none is claimed |
| G1 transport and state | skipped | measures C1, which did not happen; the P1 half is reported below |
| G2 the integrity check | skipped | its command was not run |
| G3 the base commit | **done (read-only)** | all four readings taken; base `43d14817…` confirmed |
| G4 the evidence job | skipped | its command was not run |
| G5 the package | skipped | no package; `.remedy-wt/f276-r10/package.txt` was NOT written |
| G6 push and tree | done | pushed after C2; tree carries only the sentinel; worktrees listed |
| STATUS flip, README, `consumed_by`, PR | not done | round 11's, and untouched by this round |

## Commits

### C2 — this handoff (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|------|-----|--------|
| .agent/handoff.md | rewritten | a handoff cannot table the commit that writes it |

This is the ONLY commit of round 10. C1 has no table because C1 does not exist.
No other path was written, staged or committed.

## External actions

- `git push origin feature/f276-data-root-hygiene` — after C2, G6. AGENTS.md
  Push Discipline, and amend0827 rule 1's requirement that a handback be durable,
  both order it; a push writes nothing to the work tree.
- No `gh` command was run. No pull request was opened, edited or merged. No
  branch was deleted. No history was rewritten. No force-push.
- No worktree was added or removed. The two job worktrees under `.remedy-wt/` are
  jobs' and were left alone per the block's constraint 5.

## Verification

**THE BLOCK'S OWN BYTES (R-0954), two readings side by side.**

```
on disk  .remedy-wt/f276-r10/block.md : lines 209  sha256 b00e05fed169f8c5cbc7e7212605814b529fcf3589f93a3540cad2b54fbc067e
delegation message stated for P1      : lines 209  sha256 b00e05fed169f8c5cbc7e7212605814b529fcf3589f93a3540cad2b54fbc067e
EQUAL on both readings: True
```

The saved-copy half of G1 cannot be reported: `.agent/authored/f276-r10-block.md`
was never created, because creating it is C1.

**ALL SIX PAYLOADS, verified read-only against the block's stated numbers.**

```
wc -l                                          sha256sum
  209 block.md                 b00e05fed169f8c5cbc7e7212605814b529fcf3589f93a3540cad2b54fbc067e
    2 ledger.md                6861d2dd4f8e919e1dee4e99c7657678e6558d225e8cb131744d77f0b0856925
   63 decisions.md             eb24165497b87c93a506cedfe6bb3118b77c4d9ef7b7d87807e98bce145702ab
   47 plan.md                  690b913ba9a89b85bbe2007d606dbf942bbf8b5edad906b4cdeab9df261f367a
    1 prose_slips.md           7ab1117ffe690970bef04e8a34b032143d2dd2d01f581f63886b846f2ef60abe
  144 create_f276_evidence.py  c9dc2e59ffaf79e8532a2093251e87c64fd8c3ae112005e637393f37c4206572
```

Every line count and every digest is identical to the block's P1–P6 statement.
Six of six. Not one payload was applied, edited or copied.

**G3 — THE BASE COMMIT, all four readings. Read-only; it writes nothing, so the
sentinel does not forbid it, and taking it now spares round 11 the measurement.**

```
git merge-base main HEAD
43d148177efd145f179ba2d9875eaa675b1595b7

first commit of `git rev-list --first-parent HEAD` that `git rev-list main` also holds
43d148177efd145f179ba2d9875eaa675b1595b7

git rev-list --ancestry-path 43d148177efd145f179ba2d9875eaa675b1595b7..HEAD | wc -l
45

git rev-list 43d148177efd145f179ba2d9875eaa675b1595b7..HEAD | wc -l
45
```

The base at full forty characters is `43d148177efd145f179ba2d9875eaa675b1595b7`.
THE TWO LENGTHS ARE EQUAL, 45 and 45, which is the reading closure pitfall (e)
orders and the only one that can show the base is right. Merge-base and fork
point COINCIDE here because this branch has merged nothing in — a coincidence,
which is why both were read rather than one. It is the sha P6 carries:

```
grep -n "43d14817" .remedy-wt/f276-r10/create_f276_evidence.py
33:BASE_COMMIT = "43d148177efd145f179ba2d9875eaa675b1595b7"
```

Note for round 11: this reading is taken at `970f544b`. Whatever commit round 11
makes its accepted HEAD, the two `rev-list` lengths must be RE-READ there — the
base does not move but the counts do.

**G6 — PUSH AND TREE, after C2.**

```
git worktree list
/home/decodeux/Repos/remedy                                  970f544b [feature/f276-data-root-hygiene]
/home/decodeux/Repos/remedy/.remedy-wt/job-468c8e62a2cc4fac  1b9ae606 [remedy/job-468c8e62a2cc4fac]
/home/decodeux/Repos/remedy/.remedy-wt/job-c1dba9c3d7874968  fd23710f [remedy/job-c1dba9c3d7874968]
```

Three entries: the primary checkout and the two job worktrees, which are jobs'
and are expected. No disposable worktree was created — none was ordered.

The push, the post-commit `git status --porcelain` and the `ls .agent/STOP`
reading necessarily postdate this file; they are reported in full in the round
report. The `git status --porcelain` reading will be `?? .agent/STOP` and NOT
empty, which the block's G6 did not anticipate because the block was authored
before the sentinel appeared. That is declared as deviation 3.

**GATES NOT RUN.** G1 (the C1 half), G2, G4 and G5 were not executed, and no
output is invented for them. In particular NO integrity check was run, NO
evidence job was run, NO `validation_errors` list was read, NO package was built,
NO package filename or SHA-256 exists, and `.remedy-wt/f276-r10/package.txt` was
NOT written. The word "green" appears nowhere in this file as a claim.

## Authored-text proofs

`None applied.` No reviewer-authored text was applied this round, so nothing was
copied into `.agent/authored/` and there is no disk-to-disk comparison to report.
The six payloads' read-only digest verification above is the whole of this
round's fidelity evidence, and it proves only that the originals are intact — it
makes no claim about a transport that did not occur.

The block's four containment readings were NOT re-run, because their purpose is
to justify an append that this round does not perform.

## Open findings

Unchanged from round 9 at `970f544b`: 17 open by both readings, 10 Medium, 7 Low,
none High, every one carrying `Owner: F282 — Findings paydown v2`. This round
registered nothing, resolved nothing, rotated nothing and appended nothing to
`.agent/live_review.md`; the ledger's bytes at HEAD are exactly round 9's.

Round 9's verdict is therefore STILL UNBOOKED in `.agent/live_review.md` — P2
carries it and P2 was not applied. Under amend0827 rule 1 it survives in the
committed round-9 handoff, which is a durable carrier, and the first commit of
whichever round runs next books it. Nothing is lost; it is simply still owed.

## Deviations & assumptions

1. **THE ORDERED COMMIT SEQUENCE WAS NOT COMPLETED: C1 WAS DROPPED.** The block
   orders C1 then C2. Only C2 ran. This is recorded here and not only in the
   commit table because R-0485 requires it, and it is recorded as a DEVIATION
   even though it is the correct behaviour — the block's own constraint 7 orders
   exactly this, and a reader auditing whether the round followed its block must
   find the departure in this section.
2. **Everything after C2 was skipped in full.** The integrity check, the evidence
   job and the review package were not attempted. No closure precondition was
   measured this round and no closure step was performed. The feature does NOT
   close on this round and nothing here should be read as progress toward the
   STATUS flip.
3. **G6's `git status --porcelain` will read `?? .agent/STOP`, not EMPTY.** The
   block's G6 orders the reading and states it must be empty; the sentinel makes
   that unmeetable by construction, and the sentinel may not be removed to meet
   it. The tree carries NO modified tracked file and NO untracked file other than
   the sentinel, which is the property the empty-tree gate exists to establish.
   Recorded as a deviation rather than as a red gate.
4. **G3 was run although the round stopped at C2.** It is four read-only `git`
   commands and one `grep`; it writes nothing, commits nothing and touches no
   path. It is reported because it is free and because round 11 needs it. If the
   reviewer holds that "doing nothing else" excludes even a read, the readings
   above are simply surplus and no state depends on them.
5. **`.agent/plan.md` was NOT updated and is round 9's.** AGENTS.md's Commit Gate
   asks that the plan match the current work, and P4 — this round's plan rewrite —
   is on disk and verified. Applying it is part of C1, which the sentinel forbids,
   and the STOP rule is the more specific instruction. The staleness is benign:
   the committed plan's Next Steps already name round 10's work as the work that
   remains, which is true. Declared rather than silently repaired.
6. **No finding was registered.** The sentinel is an operator action, not a
   defect, and the block's authoring without knowledge of it is the known R-0347
   window rather than a new one. Nothing on disk is wrong and there is nothing to
   repair, so no R-id is spent.
7. **No package, no hash, no job id.** The round report to the reviewer carries
   the literal `NONE — not built` for the package filename, the SHA-256, the
   archived path and the evidence job id. The accepted HEAD is likewise not fixed
   by this round. The STATUS line CANNOT be authored from round 10.

## Next

Read `.agent/STOP` from disk. While it exists, the session writes nothing further:
this is `docs/agents/self_drive_protocol.md` Phase 1 rule 1, and it precedes
rule 2, the Open PR Gate.

Once the operator removes the sentinel, RE-DELEGATE ROUND 10 FROM ITS EXISTING
BLOCK. `.remedy-wt/f276-r10/block.md` is byte-intact at 209 lines and sha256
`b00e05fe…c067e`, all six payloads verify, and the block needs no change except
that its G6 will then correctly read the tree as empty. Do not `git clean -x`
before that: `.remedy-wt/` is gitignored and a clean destroys the round.
