# Self-Drive Protocol — one-session feature building (v1)

> How ONE Claude Code session builds a Remedy feature end to end when the
> operator can only start the session and invoke a single skill.
> AGENTS.md remains the highest authority. This file changes WHO relays a
> round, never WHAT is verified. The split-workflow roles
> (docs/agents/split_workflow.md) are preserved INSIDE the session — they
> are not collapsed into one actor.

## Why this exists
From 2026-08-13 the operator reaches this machine only over SSH from a
phone. Relaying paste blocks between two windows stops being possible, so
the relay moves into the session. Everything the relay protected —
evidence-first review, block conditions, PR-only merges — stays.

## Role model inside one session (load-bearing)

| Role | Who | Writes |
|---|---|---|
| Planner & reviewer | the main session | nothing in the work tree; authors step text and findings, runs verification, issues verdicts |
| Worker | a delegated subagent, one per round | all code, docs, `.agent/` state, all commits |
| Operator | human, asynchronous | starts the session; may pull a review zip; may merge manually at any time |

The single-writer rule survives: the main session never edits a work-tree
file itself. A round in which the main session both wrote and certified
the change is a protocol violation and its verdict is void —
docs/agents/planner_reviewer_prompt.md §3 forbids self-certified
production code, and in-session delegation is how that requirement is met
once no human relay exists.

Remedy deliberately does not run self-drive as a single undivided actor:
the reviewer's independence is the only thing standing between a green
word and a green run, and it is cheaper to keep than to rebuild.

## Phase 0 — state probe (deterministic, always first)
Read-only, in this order, before any decision is made:

```bash
git status --porcelain          # must be empty
git branch --show-current
git log --oneline -n 8
gh pr list --state open --json number,headRefName,baseRefName,isDraft
remedy plan status              # F080 roadmap mirror
remedy plan next                # Rule A5 — proposes, never starts
```

Then read from disk, never from session memory: `.agent/handoff.md`,
`.agent/plan.md`, `.agent/live_review.md`, `.agent/candidates.md`, and
the active feature file under `docs/roadmap/features/`.

## Phase 1 — decide
1. `.agent/STOP` exists → write the handoff, end the session, do nothing else.
2. Open PR from a `feature/*` branch into `main`, not a draft, exactly one
   → merge it at the Open PR Gate (AGENTS.md) before any new branch.
   Anything else about that PR → stop and report.
3. `.agent/candidates.md` non-empty → the first reviewed round registers
   or resolves every entry and empties the file
   (docs/roadmap/STATUS_closure_protocol.md).
4. A handback is pending review → review it first; never plan new work
   over an ungated round.
5. Otherwise claim the next feature per STATUS order (Rule A5).

## Phase 2 — the round loop
Each round is: author → delegate → review → verdict.

Before AUTHORING each round the reviewer re-reads `.agent/STOP` from disk.
Phase 0 runs once at session start, G6 binds at any point, and a sentinel that
appears mid-session is otherwise invisible until an unrelated gate trips over
it (finding R-0347). Every block's gate list therefore also keeps a
`git status --porcelain` gate, and every handoff that names the next session's
first action names Phase 1 rule 1 before rule 2.

1. **Author.** The main session writes the step block (goal, bundle,
   exact change set, constraints, done-when with the literal verification
   commands) and any finding text, exactly as
   docs/agents/planner_reviewer_prompt.md §3 prescribes. Authored text
   that a worker will apply to a file is still saved under
   `.agent/authored/` by the worker; in-session there is no transport, so
   the hash-stamp ritual is replaced by a `cmp` of the applied file
   against the authored original — the proof obligation is unchanged.
2. **Delegate.** One worker subagent per round, given the step block and
   nothing else it did not read itself. It follows AGENTS.md in full:
   self-review loop before every commit, small commits, `.agent/plan.md`
   current, clean tree, push, handoff rewrite.
3. **Review.** The main session reads the real diff
   (`git diff <LAST_REVIEWED_SHA>..HEAD`) bottom-up and re-runs the
   round's verification commands itself. A worker's summary is never
   evidence.
4. **Verdict.** PASS → `LAST_REVIEWED_SHA` advances, next step. FAIL →
   findings persist to `.agent/live_review.md` in their own commit
   FIRST, then the repair round.

Operator amendment amend0827-process-diet (2026-08-27), rule 1 — A VERDICT
NEVER BUYS A ROUND OF ITS OWN. The committed and pushed `.agent/handoff.md`
is a durable carrier: a verdict, a finding draft or a pending registration
written there is persisted, and it is booked into `.agent/live_review.md` in
the FIRST COMMIT of the next round that is happening anyway. A round whose
entire change set is verdicts, registrations or corrections is FORBIDDEN,
with one exception — a feature's closure sequence. "Findings persist FIRST,
in their own commit" is unchanged; only the ROUND that commit belongs to
moves. Reason: 20 of F031's 70 rounds were pure bookkeeping — 106 commits between
them, 15 rounds of five commits, 4 of six and 1 of seven, and not one line
outside `.agent/` in any of them. Reverse by deleting this
paragraph.

Operator amendment amend0827-process-diet (2026-08-27), rule 5 — GATE
BUDGET. A round orders AT MOST EIGHT gates. The transport proof is ONE
digest comparison. Full byte forensics — slice reconstruction, append
arithmetic with a negative control — is reserved for production-code files
and for the append into the record; a `.agent/` prose file gets at most a
byte-equality check of the plan slice. G4 below is untouched, and mutation
red-proofs for production code stay mandatory in full: this rule spends the
forensics that were aimed at prose, nothing else.
docs/agents/planner_reviewer_prompt.md §3 carries the full wording.

Verification tiers, the canary, the integration gate and the closure
protocol are unchanged; this file adds no exception to any of them.

## Guardrails (any one trips → stop and hand off)
- **G1 PR-only merges.** Merges happen only at the Open PR Gate, only via
  `gh pr merge <n> --merge --delete-branch`. Never merge a PR this
  session created in the same session.
- **G2 Never force-push.** No `--force`, no `--force-with-lease`, no
  history rewrite, no branch deletion beyond the gate's own
  `--delete-branch`.
- **G3 Never work on `main`.** Every change lands on a `feature/*` branch.
- **G4 Gates run, never assumed.** Every commit's gate commands are
  executed and their real exit codes recorded. "Green" as a word is a
  finding.
- **G5 Destructive verification is isolated.** Mutation and red-proof
  checks run only inside a disposable `git worktree`, never in the
  primary checkout, which satisfies `git status --porcelain` == empty at
  every verdict.
- **G6 STOP file.** If `.agent/STOP` appears at any point, finish the
  current commit if one is half-written, then hand off and end.
- **G7 Session limits.** The session states its round cap and wall-clock
  cap up front and honours them. A session that ends at its limit with a
  written handoff is a SUCCESS, not a failure.
  Operator amendment amend0827-process-diet (2026-08-27), rule 6 — the
  DEFAULT plan is FOUR TO FIVE delegated rounds per session, against an
  operator target of five to seven sessions per feature. A session ends
  early ONLY on demonstrably exhausted context, or on a round that
  explicitly needs a fresh session; stopping "at a nice seam" after two
  rounds is a protocol violation, not a clean end, and G7 may not be cited
  for it. The SOFT LIMIT is 25 rounds OR 7 sessions per feature, whichever
  comes first; on reaching it the obligation is a scope report, not more
  work — see "Ending a session". Reverse by deleting this paragraph.
- **G8 Ambiguity ends the round.** Any red gate, contradiction, or
  question the rules do not answer → write the handoff and end cleanly.
  Never guess, never widen scope to route around a block.

## Ending a session
Always through `.agent/handoff.md` (F079 machinery,
docs/agents/handback_template.md): feature and round, the SESSION NUMBER of
the running feature, branch, commit SHAs, changed-files table, real
verification results, open-findings count, next expected action. The handoff
is the only return channel, and a session with no handoff did not happen. It
has no length cap (amend0827 rule 3); it is valid when its mandated sections
are present.

Operator amendment amend0827-process-diet (2026-08-27), rule 6 — AT THE SOFT
LIMIT, REPORT INSTEAD OF ROWING ON. When a feature reaches 25 rounds or 7
sessions, whichever first, the session's next obligation is a SCOPE REPORT in
the handoff: what is finished, what is missing, and a proposal — split the
remaining scope off as a DECISION, or split the feature into two STATUS lines.
The second is a DOCUMENTED PROPOSAL TO THE OPERATOR and is never executed on
the session's own authority. The session output additionally carries one
unmissable line:

    SITZUNGS-LIMIT ERREICHT — OPERATOR-BERICHT IN DER ÜBERGABE

Continuing quietly past the limit is a protocol violation. Reverse by deleting
this paragraph.

Operator amendment amend0827-process-diet (2026-08-27), rule 4 — the
pre-emission checklist of docs/agents/planner_reviewer_prompt.md §3 is FROZEN
while a feature is open. A lesson learned mid-feature goes into
`.agent/prose_slips.md` as one dated line, or into this handoff, and waits for
the single consolidation pass in the closure sequence, which may not lengthen
the list. Reverse by deleting this paragraph.

## What stays with the operator
The review zip (`scripts/make_review_zip.sh`) remains the operator's
remote window into a run, on demand and at closure. Nothing in this
protocol may assume the operator can paste anything beyond the single
command that starts the session.
