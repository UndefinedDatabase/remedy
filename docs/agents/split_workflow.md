# Split Workflow — Two-Window Feature Life Cycle (v3)

> How one feature travels from `[ ]` to `[x]` using two agent sessions on
> the same repository (CLI windows via tmux/SSH, or a chat-based reviewer).
> Manual precursor of the F070 orchestrator loop: every rule here must be
> internalizable by Remedy later. AGENTS.md remains the highest authority.

## Scope boundary (read first)
STATUS.md, docs/roadmap/, .agent/ and this workflow exist ONLY to develop
Remedy. Remedy-the-product never reads or writes these files at runtime;
its runs live exclusively in its internal data-root filesystem (see
docs/system/development-artifact-boundary-v0.md). Nothing here may leak
into product behavior. This scaffolding retires at F070/F075.

## Roles
| Window | Session | Role | Writes |
|---|---|---|---|
| 1 | top-tier model + docs/agents/planner_reviewer_prompt.md | Planner & live reviewer, one feature per session | **NOTHING — fully read-only.** Authors exact text (steps, findings, STATUS lines) applied by the worker; instructs merges. |
| 2 | worker model + bootstrap block below | Sole implementer, sole writer, executes merges via Open PR Gate on instruction | All code, docs, .agent/ state, all commits, instructed merges. |
| operator | human | Message bus + final authority | Relays prompts and handbacks; MAY manually review/merge the closure PR in the window between two features; may pull a review zip anytime. |
| external (optional) | e.g. GPT web | Second opinion via review zip | Findings return through the operator; Window 1 folds them into authored entries. |

**Single-writer rule (load-bearing):** Window 2 is the only writer, period.
It hands back only with a clean, committed, pushed branch. Window 1 reads
committed state only. Reviewer-authored text is applied verbatim; only
reviewer-authored text may set a finding to Resolved.

**Merge policy:** a closure PR is never merged in the same session that
created it. It merges at the START of the next feature via the AGENTS.md
Open PR Gate, on Window 1's instruction — the gap between features is the
operator's manual-review window. The operator may always merge manually
instead.

## Transport: git, not zips
Code moves between windows exclusively via commits on the feature branch.
The review zip (see STATUS_closure_protocol.md for the canonical build
sequence) is NOT transport — it is a frozen, manifest-verified evidence
package: mandatory at closure (referenced in the STATUS line, SHA-256
recorded), and on demand mid-feature for external second opinions.

## Round life cycle (repeat, ~1 relay per hour)
1. Window 1 turn: OPERATOR BRIEF table + exactly one paste block
   (a bundled ~45–90-min step, or a repair round). Operator relays it.
2. Window 2 implements exactly that block: AGENTS.md self-review loop,
   small commits, .agent/plan.md updated, tree clean, push. Applies any
   reviewer-authored live_review/STATUS text verbatim — findings FIRST,
   as their own commit, before fixing them.
3. Window 2 finishes in this exact order: (a) final work commits;
   (b) IF a package or gate run was instructed: attempt it NOW, from the
   clean tree; (c) rewrite .agent/handoff.md so it records the OUTCOME of
   every attempted action this round — on success the package filename +
   SHA-256, on failure the RAW error text plus a root-cause note and
   options — and commit it (for a successful package, the accepted HEAD
   remains the zip's covered head; the handoff commit above it is
   bookkeeping); (d) push; (e) completion report. A handoff that omits or
   contradicts an attempted action's result (e.g. "Next: reviewer authors
   STATUS line" after a failed build) is a block-condition violation:
   false readiness claim. Recording a failure in the handoff overrides ANY
   constraint of the round, including "no commits" — truth always wins.
   At closure specifically, the outcome-handoff may stay uncommitted after
   a successful zip and fold into the STATUS commit — the one bookkeeping
   commit above the zip's covered head (validated at the F081 closure).
4. Operator relays the report to Window 1.
5. Window 1 reviews bottom-up, verdict, next block. On closure: banner,
   session ends, PR waits for the next feature's Open PR Gate.

**Authored-text fidelity protocol (R-0147/R-0144/R-0148):** when a paste
block contains reviewer-authored text (findings, verdicts, STATUS lines,
state-file resets), each text arrives between markers of the form
`--- BEGIN <name> sha256=<hex> ---` / `--- END <name> ---`, where the
hash covers the exact bytes between the markers including the trailing
newline. The worker's FIRST action is to save each text VERBATIM from
the paste to `.agent/authored/<feature>-r<round>-<n>.md`, verify
`sha256sum` of the saved file against the marker hash BEFORE committing
— on mismatch STOP: report the mismatch and the received bytes, commit
nothing (transport-wrap guard, R-0148 class) — then commit. Applying the
text = copying from that file. Byte-identity proofs = mechanical
disk-to-disk comparison (hash or exact substring) of the applied
location against that file. A proof computed against any retyped or
reconstructed copy is a false verification claim (block condition class,
R-0147). Only reviewer-authored text — arriving this way — may write
`## Verdicts` entries or set findings Resolved.

**Duplicate-block guard (PH v3, operator ruling 2026-07-28):** on
receiving a paste block, the worker's bookkeeping FIRST ACTION also
writes `.agent/last_block.md` (overwrite; committed with the round
bookkeeping): line 1 is `OUTCOME: pending`, followed by the full
received block VERBATIM. At round end the worker updates the OUTCOME
line in place: `executed`, `refused-hash-gate`, or
`stopped-duplicate`. BEFORE executing anything, compare the received
block with the stored block portion of the previous last_block.md:
- Byte-identical and previous OUTCOME `executed` (its
  commits/artifacts are on disk) → STOP immediately, execute nothing,
  and reply only
  `##### SAME PROMPT AGAIN — PROBABLY A RELAY MISTAKE #####`
  plus one line of evidence (e.g. the existing commit shas).
- Byte-identical and previous OUTCOME `refused-hash-gate` → a LOOP:
  resending the same bytes cannot clear a hash failure. STOP with the
  same banner plus the recorded refusal evidence; do NOT re-run the
  failing verification. Absence of effects has two causes — never
  delivered, or delivered and refused — and last_block.md's OUTCOME
  line exists precisely to tell them apart.
- Byte-identical with NO previous record, or effects absent with no
  refusal recorded (a relay gap — the F048 case) → deliberate
  re-issue: proceed normally and note the re-issue in the handback.
On ANY refusal or duplicate STOP (refused-hash-gate /
stopped-duplicate), the worker COMMITS AND PUSHES
`.agent/last_block.md` — OUTCOME line set accordingly, plus one
evidence line (expected vs computed hash, or the duplicate's commit
shas) — as the round's only commit. A refusal that leaves no disk
trace is itself a handback defect. (This clarifies "committed with
the round bookkeeping" for rounds where the bookkeeping commit IS the
refusal.)

**Handback form:** every `.agent/handoff.md` rewrite follows
docs/agents/handback_template.md — all sections, in order. A missing or
incomplete section is a Medium finding; the second occurrence within one
feature is High and blocks until a compliant handback exists.

## .agent/handoff.md — the fast-resume file
Rewritten (never appended) by the worker at EVERY handback. Contains only
the latest state: feature + round, the session number of the running
feature, branch, last commit SHAs, changed-files table, verification
results (real output, trimmed), open findings count, next expected action.
Operator amendment amend0827-process-diet (2026-08-27), rule 3 — the line
tiers that stood here are WITHDRAWN; a handback is valid when it carries
its mandated sections and its length is never measured. Sections are still
never dropped. Reverse by restoring the tiers from git history at
`f4eae1d4`.
Purpose: a restarted Window 1 bootstraps from STATUS.md + feature file +
handoff.md + plan.md + live_review.md instead of re-reading the project.
Git history is the archive of past handoffs.

## Window 2 — worker bootstrap block (paste at session start)
```
You are the Remedy worker (Window 2) for feature <Fxxx>. Rules, in priority
order: AGENTS.md, then docs/agents/worker_conventions.md, then this block.
- Read docs/roadmap/STATUS.md and the <Fxxx> feature file so you know the
  plan you execute — Window 1 owns sequencing. Implement ONLY the pasted
  block, nothing beyond it.
- Branch per AGENTS.md: Open PR Gate first (merge an eligible open PR only
  when the pasted block instructs it; report raw output), then work on
  feature/<name>. Never touch main directly.
- Steps arrive as ~1-hour bundles: multiple commits expected, each small
  (<500-line diffs), full self-review loop + Commit Gate before each. Push
  after committing.
- No sub-agent fan-out: direct tool calls; at most one narrowly scoped
  delegated task. /background is fine; silent scope growth is not (A9) —
  out-of-scope needs become report items, assumptions → assumption_log.
- Reviewer-authored text (STATUS lines, live_review findings/verdicts):
  apply VERBATIM. In repair rounds: persist the findings to
  .agent/live_review.md as the FIRST commit, then fix, marking
  `Done: R-XXXX`. Never set Resolved yourself.
- Paste block contains reviewer-authored text? FIRST action: save each
  text VERBATIM to .agent/authored/<feature>-r<round>-<n>.md; verify
  sha256sum of the saved file against the sha256=<hex> in its BEGIN
  marker BEFORE committing — mismatch = STOP, report, commit nothing
  (R-0148) — then commit; apply by copying from that file; proofs are
  disk-to-disk against it (R-0147). Never write into `## Verdicts` or
  mark findings Resolved — that text only ever arrives as
  reviewer-authored files under .agent/authored/ (R-0144).
- FIRST bookkeeping action of every round: write .agent/last_block.md
  (overwrite): line 1 `OUTCOME: pending`, then the received paste
  block VERBATIM; update OUTCOME at round end (executed /
  refused-hash-gate / stopped-duplicate). If the received block is
  byte-identical to the stored one: previous OUTCOME executed → STOP,
  reply `##### SAME PROMPT AGAIN — PROBABLY A RELAY MISTAKE #####` +
  one evidence line; previous OUTCOME refused-hash-gate → STOP
  likewise (a loop — the same bytes cannot pass the gate), never
  re-run the failed check; no record / relay gap → deliberate
  re-issue: proceed and note it in the handback. On ANY refusal or
  duplicate STOP: COMMIT AND PUSH .agent/last_block.md — OUTCOME set,
  plus one evidence line (expected vs computed hash, or the
  duplicate's commit shas) — as the round's only commit; a refusal
  with no disk trace is a handback defect.
- A STOP or refusal reply contains: the banner, the evidence line(s),
  and nothing else. It never assigns tasks, questions, or
  instructions to the operator — remediation requests travel to
  Window 1 via .agent/last_block.md and the handback on disk. The
  operator relays; the operator is never the addressee of technical
  work.
- Rewrite .agent/handoff.md per docs/agents/handback_template.md — every
  section, in order.
- At every handback: in this order: commits → attempt instructed
  package/gate → handoff records the real outcome incl. raw errors +
  commit → push → report. Emit the completion report (outcome ≤6 lines,
  changed-files table, real verification output, assumption_log entries,
  deviations) ending with:
  "Handing back to Window 1 for review of <LAST_SHA>..<HEAD>."
- Never fabricate data, never imply live state over mocks, never claim
  green you did not observe. "Should work" is not a status.
- Mutation red-proofs and any other deliberately destructive
  verification run ONLY inside disposable git worktrees — never in
  the primary checkout; git status --porcelain == empty at every
  handback (R-0160 fix, operator ruling 2026-07-31; the same rule
  binds the reviewer in planner_reviewer_prompt.md §4 item 10).
```

## Session hygiene
- One feature per Window-1 session; the done-banner ends it; Rule A5 picks
  the next feature in a fresh session (token/context economy).
- .agent/live_review.md is a PER-FEATURE ledger, reset at feature start via
  an authored step; R-XXXX IDs count monotonically across features.
- Crash/compact recovery: all state survives in the repo (handoff.md,
  plan.md, live_review.md, feature-file Built State, branch commits).
  A restarted window re-bootstraps from disk; nothing from memory.
- Blocked: worker follows AGENTS.md If-Blocked; reviewer authors a finding
  routed to planning; feature may go `[!]` with reason — authored by
  Window 1, committed by Window 2.
- Autonomous multi-part blocks contain exactly ONE handback instruction —
  at the very end. Intermediate parts end with checkpoint notes inside the
  final completion report, never with a handback.
- History rewrite (rare, operator-approved only): when packaging/metadata
  validation blocks on an immutable commit (e.g. a scanner-rejected
  subject) and the operator approves a rewrite, the safe sequence is:
  (1) persist the finding + record the approval in decisions.md, own
  commit; (2) `git filter-branch --msg-filter` scoped to the exact range —
  never interactive rebase, never content edits; (3) verify: trees
  byte-identical (`git diff <old-head> HEAD` empty except intended doc
  commits) AND a metadata re-scan comes back clean — any content delta is
  a hard STOP; (4) `git push --force-with-lease`, allowed ONLY on an
  unmerged solo feature branch, never on main or shared branches;
  (5) rebuild the evidence bundle and package at the NEW head — all prior
  SHAs in ledgers/handoff refer to pre-rewrite history and the accepted
  HEAD becomes the new zip head. Content-identity means no re-review is
  required; the verdict transfers.

## Sunset
F070 replaces the operator-as-message-bus; F075 (10 flawless self-runs) is
where the operator moves from relaying to testing. When F070 lands, this
round life cycle becomes the orchestrator's reference behavior and the
paste blocks become prompt segments. Do not let this file drift from
docs/agents/ conventions.
