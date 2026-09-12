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

Operator amendment amend0905-throughput (2026-09-05) — LEDGER ROTATION.
`.agent/live_review.md` is rotated by `scripts/rotate_live_review.py` as its
own commit inside EVERY closure sequence, after the verdict bookings and
before the STATUS flip: every `Gate:` record whose feature id is `[x]` in
`docs/roadmap/STATUS.md`, and every resolved finding pair (the `- R-xxxx`
registration block with its one matching `Done: R-xxxx` block), moves
byte-verbatim into the append-only `.agent/live_review_archive.md`, which
the script verifies by per-record sha256 before and after and refuses on any
mismatch; the open-findings count is identical before and after. The byte-
append arithmetic of the next round's block re-baselines on the
post-rotation length. The archive is never read at session start — only on
demand, by id. Rationale: the ledger had grown to ~2.5 MB, most of it
per-round `Gate:` records of long-closed features, and every bootstrap paid
for it. Reverse by deleting this paragraph.

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
  Operator amendment amend0905-throughput (2026-09-05) — SESSIONS CONTINUE
  WHILE CONTEXT COMFORTABLY SUFFICES. The target is SIX TO EIGHT delegated
  rounds per session; four remains the floor. The honest early-end reasons
  above are unchanged — demonstrably exhausted context, or a round that
  explicitly needs a fresh session — and now explicitly include the
  reviewer noticing its own authoring errors accumulating (a run of
  `.agent/prose_slips.md` lines in one session is that signal). Every
  handoff adds ONE sentence of context self-assessment in its Session
  section. Rationale: each session boundary re-buys the full cold start —
  protocol, handoff, ledger, decisions — and F109's session 4 already ran
  eight PASS rounds, so the four-to-five default was spending boundaries
  the context did not need. Reverse by deleting this paragraph.
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

Operator amendment amend0905-throughput (2026-09-05) — THE STANDING DEFAULT AT
THE SOFT LIMIT IS SPLIT-AND-CLOSE, EXECUTED BY THE SESSION. On reaching the
soft limit the session still writes the scope report, and then EXECUTES the
default on its own authority: it registers the remaining scope as a new
follow-up feature (registration only, ledger atomicity respected — the
`TOTAL_FEATURES` pin, the README counters and the STATUS line in one commit
with the feature file), closes the current feature at a self-consistent
scope through the normal closure sequence, and records the whole move as a
dated DECISION in `.agent/decisions.md` that the operator may reverse
afterwards. The banner line stays but announces the REPORT, not a stop.
Only when no self-consistent close is possible does the old hard stop with
an operator question remain. This applies equally to a feature found
already past its limit with a pending scope report at session start.
Rationale: F262's round 23 wrote a correct scope report and then waited a
session for a ruling the default would have supplied. Reverse by deleting this paragraph.

Operator amendment amend0906-split-placement (2026-09-06) — A FOLLOW-UP FEATURE
SPLIT OFF AN OPEN FEATURE IS PLACED DIRECTLY AFTER ITS PARENT. When a session
registers the remaining scope of feature F<p> as a new feature F<q>, the new
STATUS line goes IMMEDIATELY after F<p>'s line, inside the same tier heading
(the filename tier follows the enclosing heading, as the docs test pins), so that
Rule A5 proposes F<q> before any other unchecked feature. Every open feature file
that names F<p> in its "Depends on" line gains F<q> there in the same commit, and
F<q>'s file names the parent, the closure evidence it starts from, and the exact
T-slices carried over — copied from the parent's file, not re-planned. The
parent's file states in its Built State which slices moved to F<q>. Reverse by
deleting this paragraph.

Operator amendment amend0906-triage-throughput (2026-09-06) — DELETION ROUNDS AND
THE F272 LIMIT. (1) A DELETION ROUND is a round whose change set contains no
edited line under packages/, apps/ or tests/ — only deleted files, deleted
catalog entries, deleted cockpit sections and the test/import edits those
deletions force. A deletion round is verified by four measurements and nothing
else: the import-reachability test green, the full suite green, a repo-wide
grep for every deleted module and symbol at zero, and ruff clean on the touched
files. No byte-arithmetic transport, no per-file reconstruction, no mutation
red-proof of deleted code. The block for a deletion round is at most sixty
lines and lists the paths; a whole deletion list may be one round. (2) F272's
soft limit is 12 sessions and 40 rounds, by operator order, because it was
measured before registration as the largest feature of the block and a second
split would only mint F274 with the same remainder; the split-and-close default
still applies at 12/40. (3) The session round target of 6 to 8 stands; a session
ending below it states the reason in one sentence in its handoff. Reverse by
deleting this paragraph.

Operator amendment amend0911-feedback (2026-09-11), rule A — FINDINGS ARE NEVER
WITHOUT AN OWNER AND ARE NEVER LOST. Every open finding has exactly one owner:
the feature it was found in (when the repair is in that feature's scope), a named
future feature (when the repair is inside that feature's planned scope — the
reviewer writes `Owner: F<n>` at the end of the registration line and the owning
feature's file gets ONE Acceptance line naming the id, in the same commit), or,
by default, the next findings-paydown feature. Assignment never resolves a
finding; only the owning feature's closure resolves it, with evidence. A finding
whose owner closes without it is re-assigned to the next paydown feature in that
closure's own commit, never silently carried. Reverse by deleting this paragraph.

Operator amendment amend0911-feedback (2026-09-11), rule B — ROLLING PAYDOWN,
ONE PER FIVE FEATURES. There is always exactly one unclaimed findings-paydown
feature in `docs/roadmap/STATUS.md`. When a paydown feature closes, its closure
sequence registers the next one, `F<next id> — Findings paydown v<N+1>`, placed
exactly five `[ ]` lines below the position the closing feature held (after the
next five unaccepted features), under a `## Tier 2` heading — inserting a heading
`## Tier 2 — Findings paydown (rolling, operator rule amend0911-feedback)` directly
above the line when the fifth slot falls under another tier — with the
`TOTAL_FEATURES` pin in `tests/docs/test_docs_consistency.py` and the README
counter in the SAME commit, as its own step before the STATUS `[x]` flip. A
paydown feature's file is registered THIN and filled at CLAIM: its first round
reads the open set and writes the slice list (one slice per module, the finding
text is the spec) from every open finding registered before the claim date whose
text describes a repair that fits one round; what does not fit stays open, keeps
its owner line pointing at the next paydown, and is named in the file as carried.
A paydown feature's soft limit is 8 sessions; at the limit it closes with what is
resolved and carries the rest, which is not a split and registers nothing extra.
F273 is v1 and closes F273 as written plus its T016; the first rolling
registration happens at F273's closure. Reverse by deleting this paragraph.

Operator amendment amend0911-feedback (2026-09-11), rule C — THE OPERATOR
QUESTIONS FILE. `.agent/operator_questions.md` is the one place a session puts
what it needs the operator to know or decide; it is read by the operator with one
command and by the orchestrator at every relay. Two kinds of entry: (A) a question
the session could not decide under decide-and-proceed — the old "hard stop with an
operator question" and every carried doubt; (B) a REVERSIBLE ruling the session
DID make that changes user-visible behaviour, priority order, budget or a safety
gate, and that the operator may overturn. Each entry: a heading
`### Q<n> — <five-word title> (<date>, F<n>, round <n>)` for the record, then a
body that stands alone — "What needs deciding", "Why it matters", "My
recommendation", "What happens if you say nothing" — in plain full sentences,
without finding ids, round numbers, decision ids or file paths inside the body;
a reader who knows nothing about the round must be able to decide from the body.
Soft cap FIVE: above five, the session first condenses the entries of lowest
impact into one and never drops one; urgency is the reason the cap is soft. A
session writes or updates the file in its handback commit through the worker
(the reviewer stays read-only), and the handoff's `## Next` states the count
("Operator questions open: <n>"). Entries leave the file only by the operator's
answer: the operator's next amendment records the answer as a dated DECISION and
deletes the entry in the same commit. The empty file reads exactly
`EMPTY — nothing is waiting on the operator.` under its header. The §3 checklist
of `docs/agents/planner_reviewer_prompt.md` is untouched by this rule (amend0827
rule 4). Reverse by deleting this paragraph and the file.

Operator amendment amend0911-f275-to-scope (2026-09-11, folded into
amend0911-feedback) — F275's soft limit of 20 sessions and 60 rounds
(amend0908-f275-finish rule 1) is LIFTED without a replacement number, by
operator ruling of 2026-09-11: F275 closes only at full scope (the atomic record
flip, the resolver collapse, the closure sequence), however long that takes. No
scope report, no session-limit banner and no limit line is owed any more; rules 2
to 5 of amend0908-f275-finish stand unchanged. This paragraph overrides the two
amend0908 paragraphs in `docs/roadmap/features/T2_F275.md` wherever they state the
numbers; those paragraphs stay byte-identical as history. Reverse by deleting this
paragraph.

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
