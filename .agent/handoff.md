# Handback — F040 · SESSION 3 · round 10 — STOPPED ON THE `.agent/STOP` SENTINEL

> Written by the WORKER as the round's ONLY commit. The bundle C0a through C6 was
> NEVER MADE. `.agent/STOP` was present on disk when it was read before the first
> commit, so block constraint 12, `docs/agents/self_drive_protocol.md` Phase 1
> rule 1 and guardrail G6 all ordered this round to stop before C0a. No gate of
> the block was run, and no exit code is claimed for one. Every number below that
> IS a measurement was taken from `subprocess.run(...).returncode` or from a
> Python `os.stat` / `hashlib` read inside `.remedy-wt/r10_stop_probe.py` and
> `.remedy-wt/r10_handback_inputs.py`; not one was read through a pipe or from
> `$?`.

## Session

SESSION 3 of feature F040 · round 10 · rounds so far 10.

The soft limit (25 rounds / 7 sessions, amend0827 rule 6) is NOT approached at 10
rounds and 3 sessions, so no scope report is owed and no session-limit line is
emitted.

## Why this round shipped nothing

`.agent/STOP` EXISTS ON DISK AND WAS RAISED AGAINST THIS ROUND, not left over
from an earlier one. Measured before the first commit:

| Reading | Value |
|---|---|
| exists | True |
| size | 0 bytes |
| sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (the empty string) |
| mtime | `2026-08-29T20:22:43` |
| HEAD `5778fccb` committed at | `2026-08-29T20:10:53+02:00` |
| `git ls-files .agent/STOP` | 0 lines — untracked |
| `git log -- .agent/STOP` | 0 lines — NEVER tracked, in the whole history |
| `git check-ignore -v .agent/STOP` | exit 1 — NOT gitignored |

The mtime is 11 minutes and 50 seconds LATER than the round 9 handback commit
that closed the previous round, so the sentinel appeared AFTER round 9 finished
and is therefore addressed to round 10. That is the reading finding R-0347 and
the F031 R10 entry both call for.

THREE INDEPENDENT RULES ORDER THE SAME BEHAVIOUR, and none of them admits an
exception here:

- block constraint 12 — "RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT
  AND AGAIN BEFORE C7. If it appears, finish the commit in hand, write the
  handback and stop." No commit was in hand: the sentinel was read BEFORE C0a.
- `docs/agents/self_drive_protocol.md` Phase 1 rule 1 — "`.agent/STOP` exists →
  write the handoff, end the session, do nothing else."
- guardrail G6 — "If `.agent/STOP` appears at any point, finish the current commit
  if one is half-written, then hand off and end."

THE SENTINEL WAS NOT DELETED and was not committed. Finding R-0347 forbids
removing it, and it is the operator's to clear.

## Range

Review of `5778fccb`..`HEAD` on branch `feature/f040-completion-digest`. The base
is round 9's handback commit and was the tip of the branch when this round
opened. The range is ONE commit, this handback. No branch was cut or deleted, no
pull request created or merged, nothing force-pushed, no commit touched `main`,
and no worktree was created.

## Commits

### C7 — this commit (self-reference, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this file | C7 — a handoff cannot table the commit that writes it, and §3 item 14 does not order its own insertion count |

NO OTHER PATH MOVED. C0a, C0b, C1, C2, C3, C4, C5 and C6 were never made, so
`.agent/authored/f040-r10.md` does not exist, `.agent/last_block.md` still holds
the ROUND 9 block at sha256
`fcfd0b131dec41599c12e9b67453c14a2170b0d541a3a79aec545ca1b40cc723` over 24159
bytes, `.agent/plan.md` and `.agent/live_review.md` are unmoved, and neither
`apps/ui/src/components/digest/DigestHeroCard.tsx` nor
`tests/ui_contracts/test_digest_hero_card.py` was created — both read False on
disk. `apps/ui/src/components/metrics/TopMetricsBar.tsx` and
`apps/ui/src/api/digestCardCopy.test.ts` were read and NOT edited.

The block's per-commit insertion counts are therefore not orderable and are not
claimed. G8's `git diff --numstat` sweep, which is where
`docs/agents/handback_template.md`'s `+/-` column would have been sourced from,
did not run because the commits it measures do not exist.

## External actions

| Command | Outcome |
|---|---|
| `git push -u origin feature/f040-completion-digest` | run after this commit |

No `git worktree add` and no `git worktree remove`: destructive verification was
never reached, so no disposable worktree was created. `git worktree list` reads
ONE line, the primary checkout, and read one line at every point this round. No
`gh` command was run, no pull request was created, edited or merged, no branch was
deleted, nothing was force-pushed and no history was rewritten. The `remedy`
script was not invoked.

## Verification

### THE ORDERED GATES — G1 THROUGH G8 — WERE ALL **NOT RUN**

Each is anchored by the block to a commit that this round did not make. No exit
code is reported for any of them, because none was produced. "Green" is not
claimed, and neither is red.

| Gate | Anchored at | Status | Reason |
|---|---|---|---|
| G1 transport | C0b | NOT RUN | C0a and C0b never made; `.agent/authored/f040-r10.md` does not exist |
| G2 the plan | C1 | NOT RUN | C1 never made; PLAN10 was not applied |
| G3 the record append | C2 | NOT RUN | C2 never made; RECORD10 was not appended |
| G4 the ledger | C2 | NOT RUN | C2 never made; the ledger did not move |
| G5 the component's shape | C5 | NOT RUN | C5 never made; `DigestHeroCard.tsx` does not exist |
| G6 the guard and its red proof | C6 | NOT RUN | C6 never made; `test_digest_hero_card.py` does not exist |
| G7 R-0756 repaired, and proved | C4 | NOT RUN | C4 never made; `digestCardCopy.test.ts` is unedited |
| G8 the suites, the toolchain and the tree | C6 | NOT RUN | C6 never made |

### THE READINGS THAT DID RUN — the STOP decision's own evidence

These are NOT the block's gates. They are the read-only probe that established
the sentinel's presence and provenance, and the state readings this handback
reports. Both drivers live under the gitignored `.remedy-wt/`.

    + python3 -B .remedy-wt/r10_stop_probe.py
    .agent/STOP exists: True | size 0 | mtime 2026-08-29T20:22:43
    sha256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    git ls-files .agent/STOP          REAL EXIT CODE 0 | 0 lines (untracked)
    git log -- .agent/STOP            REAL EXIT CODE 0 | 0 lines (never tracked)
    git check-ignore -v .agent/STOP   REAL EXIT CODE 1 (NOT ignored)
    git log -1                        REAL EXIT CODE 0
      5778fccbfd2848878aeb7687bd05890c5d853d2c 2026-08-29T20:10:53+02:00
    git status --porcelain            REAL EXIT CODE 0 | 1 line: '?? .agent/STOP'
    git ls-files --others --exclude-standard  REAL EXIT CODE 0 | count 1
    git worktree list                 REAL EXIT CODE 0 | 1 line
    git branch --show-current         REAL EXIT CODE 0 | feature/f040-completion-digest

    + python3 -B .remedy-wt/r10_handback_inputs.py
    .remedy-wt/f040-r10-block.md  sha256 ba22aa3a0626f66db5736a25f5fedf3ea10b47cb053aeb7f45c483f6e5a22dfd
                                  30756 bytes, 358 lines
    .agent/authored/f040-r10.md   on disk False | git ls-tree HEAD -> empty
    .agent/last_block.md          sha256 fcfd0b13... 24159 bytes (still the R9 block)
    .agent/live_review.md         1710202 bytes, UNMOVED
      registered '^- R-\d+ — ' 316 occurrences, 316 distinct, max R-0755
      resolved   '^Done: R-\d+' 56 occurrences, 54 distinct
      OPEN COUNT 262
      '- R-0756 — ' line-anchored: 0   (R-0756 is NOT yet registered)
      '^Gate: F040 R\d+ — ' keys: [1,2,3,4,5,6,7,8]  — R9 is NOT yet booked
      DECISION F040 keys: D1..D10
    DigestHeroCard.tsx exists: False | test_digest_hero_card.py exists: False
    STOP re-read immediately before the handback: True

THE BLOCK SURVIVED INTACT AND IS RE-DELEGATABLE UNCHANGED. The reviewer's own
original at `.remedy-wt/f040-r10-block.md` verifies against the digest the order
stated — sha256
`ba22aa3a0626f66db5736a25f5fedf3ea10b47cb053aeb7f45c483f6e5a22dfd` over 30756
bytes — checked before it was read and again when this handback was written.

### THE TWO ITEMS THE RECORD IS STILL OWED, carried forward unchanged

Neither is this round's to fix now, and both must land in the FIRST commit of
whichever round runs next (amend0827 rule 1, the durable-carrier clause):

1. THE R9 VERDICT is not in `.agent/live_review.md`. `^Gate: F040 R9 — ` reads 0
   lines and the booked keys run R1 to R8 only.
2. R-0756 is not registered. `- R-0756 — ` reads 0 line-anchored occurrences and
   the maximum id in the record is still R-0755.

Both texts are authored and preserved verbatim as the RECORD10 slice inside
`.remedy-wt/f040-r10-block.md`, so nothing is lost and nothing needs re-authoring.

## Authored-text proofs

NONE APPLIED. No slice was extracted and no slice was applied, because the commits
that would have carried them were never made. PLAN10 and RECORD10 remain only
inside the reviewer's own block file, whose digest is verified above.

## Item status

| Item | Status | Reason |
|---|---|---|
| C0a save the block to `.agent/authored/f040-r10.md` | skipped | `.agent/STOP` present before the first commit |
| C0b mirror the block into `.agent/last_block.md` | skipped | same |
| C1 rewrite `.agent/plan.md` from PLAN10 | skipped | same |
| C2 append RECORD10 to `.agent/live_review.md` | skipped | same |
| C3 export the two estimate constants (TMB-1, TMB-2) | skipped | same |
| C4 repair R-0756 in `digestCardCopy.test.ts` | skipped | same |
| C5 create `DigestHeroCard.tsx` | skipped | same |
| C6 create `tests/ui_contracts/test_digest_hero_card.py` | skipped | same |
| C7 rewrite `.agent/handoff.md` | done | this file — the ordered stop behaviour |
| G1 transport | skipped | anchored at C0b, which was never made |
| G2 the plan | skipped | anchored at C1, which was never made |
| G3 the record append | skipped | anchored at C2, which was never made |
| G4 the ledger | skipped | anchored at C2, which was never made |
| G5 the component's shape | skipped | anchored at C5, which was never made |
| G6 the guard and its red proof | skipped | anchored at C6, which was never made |
| G7 R-0756 repaired, and proved | skipped | anchored at C4, which was never made |
| G8 the suites, the toolchain and the tree | skipped | anchored at C6, which was never made |

## Deviations & assumptions

1. THE ENTIRE ORDERED COMMIT SEQUENCE WAS DROPPED — the largest possible
   departure from block constraint 2, declared here as
   `docs/agents/handback_template.md` requires and not only in the commit table.
   C0a, C0b, C1, C2, C3, C4, C5 and C6 were all skipped and only C7 was made. The
   justification is block constraint 12 read together with Phase 1 rule 1 and G6:
   a clause naming a terminating condition wins over the sequence it terminates.
   This is the F031 R10 and F031 R34 precedent, each of which stopped on the same
   sentinel before its first commit and each of which was graded PASS on its
   conduct.
2. `git status --porcelain` READS ONE LINE, NOT THE ORDERED ZERO. That line is
   `?? .agent/STOP`, the sentinel itself. Constraint 11 wants an empty porcelain
   at every commit, and an empty porcelain is UNREACHABLE while the sentinel
   stands, because finding R-0347 forbids deleting it and committing it would be
   outside the change set. The conflict is declared rather than resolved by
   deletion. `git ls-files --others --exclude-standard` counts 1 for the same
   single reason; no scratch file leaked, since both drivers live under the
   gitignored `.remedy-wt/`.
3. `.agent/plan.md` IS STALE AND WAS DELIBERATELY LEFT SO. It still reads
   "SESSION 2, round 9" and still describes round 9's work as "this round". C1 is
   what would have corrected it, and C1 was not made. Writing self-composed text
   into it instead of the authored PLAN10 slice would substitute the worker's
   words for the reviewer's, and applying PLAN10 outside its ordered commit would
   break constraint 2 — so the conservative reading is to touch nothing. This is
   the same call F031 R34 made and the reviewer endorsed. It is repaired by
   whichever round runs the block next.
4. NO SLICE WAS APPLIED, so constraint 1's apply-anyway-and-object clause was
   never exercised. ONE OBSERVATION FOR THE REVIEWER, offered as a reading and not
   as an objection: PLAN10's `## Current Step` table marks "T002 the card
   component and its guard" as `done | this round`, which is a forward-looking
   claim that is now false of round 10. If the block is re-delegated unchanged the
   claim becomes true again the moment the bundle actually lands, so no edit is
   needed — but if the reviewer instead re-numbers the round, that cell and the
   "SESSION 3, round 10" line are the two places in PLAN10 that carry a round
   number.
5. THE ROUND NUMBER IS LEFT TO THE REVIEWER. This round has landed a commit and
   would ordinarily earn the ledger key `Gate: F040 R10`. The F031 R10 entry ruled
   that the number must MOVE FORWARD in exactly this situation, so that a re-run
   of the same block does not put two paragraphs under one key — the §3 item 26
   defect finding R-0587 registers. That is a numbering ruling and belongs to the
   reviewer, not to the worker, so this handback states the precedent and makes no
   ruling.
6. NO GATE WAS RUN AND NO SUITE WAS EXECUTED. Phase 1 rule 1 says "do nothing
   else", and running the G8 suites at the base would have been work the stop
   order forbids rather than evidence the block asked for. The read-only probe
   above is the STOP decision's own evidence and is labelled as not being a gate.
7. `.agent/context.md`, `.agent/decisions.md` AND `.agent/prose_slips.md` WERE NOT
   TOUCHED. None is in the block's change set, and the R9 verdict's two dated
   prose-slip lines are the NEXT round's to append, at the round that writes one.
8. NO DOCUMENTATION UNDER `docs/` WAS UPDATED. This round ships no behaviour at
   all, so the commit gate's item 8 is answered rather than skipped.
9. THE OPEN PR GATE WAS NOT RUN. Phase 1 rule 1 precedes rule 2 and fires first,
   ending the round before the gate is reached; no branch was created, which is
   the only thing that gate stands in front of.

## Open findings

262, UNCHANGED — computed at HEAD as 316 distinct registered ids minus 54 distinct
resolved ids. This round registers none and resolves none.

R-0756 IS NOT AMONG THEM. It is drafted in the block's RECORD10 slice and, per
amend0827 rule 1, is carried durably there and in this handback; it is booked into
`.agent/live_review.md` by the first commit of the next round. Counting it before
it is written would misstate the record.

- R-0570 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0752 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0755 — OPEN, routed to the paydown branch. Not F040's to fix.
- R-0753 — OPEN, carried as this feature's documented risk.

## Next

THE OPERATOR CLEARS `.agent/STOP`. Nothing else can proceed while it stands, and
no agent may remove it (finding R-0347).

Once it is cleared, the next session's FIRST action is Phase 1 rule 1 — re-read
`.agent/STOP` from disk before anything else — and then rule 2, the Open PR Gate.

The work order is UNCHANGED AND READY TO RE-DELEGATE AS IT STANDS:
`.remedy-wt/f040-r10-block.md`, sha256
`ba22aa3a0626f66db5736a25f5fedf3ea10b47cb053aeb7f45c483f6e5a22dfd` over 30756
bytes and 358 lines. Its bundle — the two estimate-constant exports, the R-0756
repair, `DigestHeroCard.tsx`, its pytest guard, PLAN10 and RECORD10 — is entirely
unstarted, so it needs no rewrite. The one thing the re-run must ALSO carry, in
its first commit, is the pair the record is still owed: the R9 verdict under the
key `Gate: F040 R9 — ` and the registration of R-0756. Both are already authored
inside that block as the RECORD10 slice.
