── STEP CLOSE THE HANDOFF LOOP / F040 — ROUND 21 ─────────────
Goal:        Round 20's `.agent/handoff.md` was necessarily frozen at C3,
             before its own C4 (the candidates-only commit) and the PR
             existed — it defers the C4 SHA and the PR number to "the
             round report," which is the worker's chat reply to the
             reviewer and is NOT a disk artifact. self_drive_protocol.md's
             own words are "the handoff is the only return channel, and a
             session with no handoff did not happen"; a fact that exists
             only in an agent-to-reviewer chat transcript does not survive
             a context reset. This round makes the handoff self-contained
             by APPENDING an addendum with the two facts the reviewer
             independently verified: the C4 SHA and the PR's number/URL/
             state. Per "a correction carries the old fact"
             ([[feedback_correction_carries_the_old_fact.md]] in spirit),
             the original round-20 record is NOT edited or overwritten —
             only extended.

Bundle:      C0a save this block verbatim · C0b mirror it · C1 the addendum
             append to `.agent/handoff.md`.
Change:      EXACTLY these paths and nothing else.
               `.agent/authored/f040-r21.md`               (C0a, new)
               `.agent/last_block.md`                       (C0b)
               `.agent/handoff.md`                          (C1)
             NOTHING ELSE IS TOUCHED. No `.agent/plan.md` rewrite this
             round (there is no next step to describe — F040 is closed;
             rewriting `plan.md` for a closed feature would be a stale
             artifact the next feature's claim round would just replace
             anyway). No `.agent/live_review.md` append this round either
             — this round adds no new verdict of its own; it completes the
             PREVIOUS round's own already-PASSED handback with facts that
             round's own C3 could not yet know. `docs/roadmap/STATUS.md`,
             `README.md`, `.agent/candidates.md` and the PR are UNTOUCHED —
             all three are already correct and independently verified by
             the reviewer; this round adds no new claim about any of them
             beyond quoting the two facts named above.

Constraints:
 1. THE COMMIT ORDER IS C0a, C0b, C1 and it is fixed.
 2. THE ADDENDUM IS APPENDED to `.agent/handoff.md`, never inserted or
    used to edit an existing line. Measure the pre-commit byte length and
    trailing-newline state directly; do not assume them (report: 14565
    bytes, trailing newline True — the reviewer's own measurement,
    confirm it matches fresh). The append is pure concatenation: base +
    one newline + ADDENDUM's own bytes.
 3. THE TWO FACTS IN THE ADDENDUM ARE GIVEN, NOT DISCOVERED, this round —
    the reviewer already independently verified both by reading disk and
    `gh pr view` directly: C4 is commit `5ec85b07` (path set exactly
    `.agent/candidates.md`, confirmed against the committed diff); the PR
    is #225, `https://github.com/UndefinedDatabase/remedy/pull/225`,
    base `main`, head `feature/f040-completion-digest`, `isDraft: false`,
    `mergedAt: null`. Re-confirm both fresh with `git show --stat 5ec85b07`
    and `gh pr view 225 --json number,state,isDraft,baseRefName,
    headRefName,mergedAt,url` immediately before writing the addendum, and
    declare in this round's own report if either has changed since (a
    changed `mergedAt` would mean the PR was merged between rounds, which
    would itself be worth flagging loudly since G1 of self_drive_protocol.md
    forbids this session from doing that merge).
 4. RE-READ `.agent/STOP` FROM DISK BEFORE THE FIRST COMMIT AND AGAIN
    BEFORE C1 (the only content commit). If it appears, finish the commit
    in hand and stop — there is nothing else queued this round regardless.
 5. PUSH after C1. Create no PR (one already exists), merge nothing,
    force-push nothing.

Done when: every gate below is executed, each with its REAL exit code or
REAL measured value.

 G1 TRANSPORT, at C0b. sha256 and byte length of
    `.remedy-wt/f040-r21-block.md`, `.agent/authored/f040-r21.md` and
    `.agent/last_block.md`; all three equal.
 G2 THE APPEND, at C1. Re-measure the pre-commit length rather than taking
    it from this block. `base + "\n" + ADDENDUM == committed`, byte for
    byte. Negative control, inside a disposable worktree: flip one byte
    inside ADDENDUM's own first paragraph and report that the
    reconstruction check REJECTS it and ACCEPTS the unflipped bytes.
 G3 THE TWO FACTS, at C1. Fresh `git show --stat 5ec85b07` output showing
    exactly `.agent/candidates.md` as the only changed path; fresh
    `gh pr view 225 --json number,state,isDraft,baseRefName,headRefName,
    mergedAt,url` output, reported verbatim, with `mergedAt` explicitly
    called out as null or not.
 G4 THE TREE, at C1/after. `git status --porcelain` empty; `git worktree
    list` one line; branch pushed and matching `origin` at C1.

Handback:    a short chat report is sufficient this round (this is a
             one-commit addendum, not a full handback-template round) —
             report the C1 SHA, confirm G1-G4, and confirm the push. No
             `.agent/handoff.md` REWRITE is needed after C1, since C1 IS
             the completion of the existing handback (an append, not a
             replacement) — rewriting it again would just re-create the
             same self-referential gap this round exists to close.
──────────────────────────────────────────────────────────────

<<<BEGIN ADDENDUM

## Addendum (round 21) — the two facts round 20's own C3 could not yet know

Round 20's handback (this file, as committed at `0ec9bb37`) named C4 and the
pull request as "pending," deferred to "the round report" — the worker's
chat reply to the reviewer, which is not a disk artifact and does not
survive a context reset. Both facts are now confirmed and recorded here,
independently, by the reviewer:

**C4** is commit `5ec85b07` — `docs(f040): record the F033 closure
candidate`. Its changed-path set is exactly `.agent/candidates.md`, matching
round 20's own constraint 8 and DECISION amend0827 D2 (a candidates-only
commit is the one permitted successor to the closure commit). G7 (the
candidate) reads PASS: `.agent/candidates.md` was empty at this round's
base and the committed file names the F033 README-paragraph gap, F040 as
the source feature, and 2026-08-30 as the date, with no `R-` id spent.

**The pull request** is **#225** —
`https://github.com/UndefinedDatabase/remedy/pull/225` — head
`feature/f040-completion-digest`, base `main`, `isDraft: false`,
`mergedAt: null`, state `OPEN`. G8 (the tree and the PR) reads PASS: the
tree is clean, `git worktree list` shows one line, the branch is pushed and
matches `origin`, and the PR is open, non-draft, and unmerged, exactly as
self_drive_protocol.md's G1 guardrail requires of a PR opened in the
session that opened it.

F040's own build is complete on disk. The merge itself is deferred to the
Open PR Gate (AGENTS.md; STATUS_closure_protocol.md algorithm step 6): the
next session that runs Phase 0's state probe finds PR #225 via
`gh pr list --state open` independently of this addendum, and merges it
before claiming any new feature, per self_drive_protocol.md Phase 1 rule 2.
This addendum exists so that fact is also readable from this file alone,
without depending on any chat transcript surviving.
<<<END ADDENDUM
──────────────────────────────────────────────────────────────
