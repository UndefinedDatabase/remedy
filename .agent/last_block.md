OUTCOME: executed
── STEP PH-v4/1 — four process rulings, docs only ──────────────────
Context:     Chore round (no STATUS.md change). Rules, in priority
             order: AGENTS.md, docs/agents/worker_conventions.md,
             the worker bootstrap block in
             docs/agents/split_workflow.md.
Goal:        Persist four operator-accepted process rulings (PH v4)
             as docs-only amendments; open a PR; do NOT merge.
Branch:      Open PR Gate first: `gh pr list --state open` must be
             empty (report raw output). Then from clean, current
             main (bcc7ede): git checkout -b chore/process-hardening-v4
Change:      ONLY docs/agents/planner_reviewer_prompt.md,
             docs/agents/split_workflow.md, and .agent/** bookkeeping.
Constraints: Each authored text below: save VERBATIM to
             .agent/authored/phv4-r1-<n>.md, verify sha256sum against
             the BEGIN marker BEFORE committing — mismatch = STOP,
             report expected vs computed hash and the received bytes,
             commit nothing. Duplicate-block guard: previous
             .agent/last_block.md has OUTCOME executed and these are
             new bytes → normal execution; note this in the handback.

PROCEDURE (steps 1-6 as received; authored texts follow verbatim)

--- BEGIN phv4-r1-1 sha256=a922959232ce7ee36edefceb45ecace758c3bd4e2e010cc40671edf97e18e0d1 ---
**Paste-block format (PH v4, operator ruling 2026-07-28):** the paste
block is ALWAYS the LAST content of the reply — nothing after it,
ever; recaps and notes go before it. The ENTIRE block is emitted
inside a fenced code block so no markdown renderer on the relay path
can mutate its bytes (PH v3 lesson: an unfenced emission had heading
markers, blockquote markers and leading indentation stripped in
transit — every authored hash in it broke). The FIRST line inside the
fence is the single top separator, exactly:
━━━━━━━━━━━━━━━━━━━━ ✂ PROMPT — copy everything below ━━━━━━━━━━━━━━━━━━━━
Copy starts on the NEXT line; the separator's glyphs never touch the
copied bytes. There is NO bottom delimiter — the block ends at the
closing fence, which is unambiguous because nothing may follow the
block. SEPARATOR LINE ONLY — never side borders or per-line
prefixes: any character added to a content line becomes part of the
copied bytes and breaks every sha256 in the block. Authored texts
appear ONLY inside that single block, exactly once per reply;
rendering an authored text or the block region twice in one reply is
a defect of the reply, treated like a transport fault (F251-R3
lesson: a duplicated, truncated render broke an authored hash
unrecoverably).
--- END phv4-r1-1 ---

--- BEGIN phv4-r1-2 sha256=4716a3d34cea670681e4cea486a411ecea68f3b425ddb8848b7dffa02dc225ec ---
**(3) Exactly ONE paste block** for the worker. Never zero, never two.
Sole exception: a hard STOP for an irreversible-destructive action
(history rewrite, force push, deletion of operator data) or a genuine
AGENTS.md contradiction with no conservative reading — and even a
STOP ships the best prepared paste block for the moment it lifts,
plus the reviewer's already-made recommendation. The operator is
NEVER asked a question, offered a menu, or handed a ruling request.
--- END phv4-r1-2 ---

--- BEGIN phv4-r1-3 sha256=bd2841983c8f32009e0c02069a342b164ee94b8091f033ae5c29b86ec92dc94b ---
"Läuft's rund?" is binary and simple: ✅ = each round closes items and
nothing previously fixed comes back. ⚠️ = the same problem needs fixing a
second time, or a round ends with as many/more open findings than it
started with. On ⚠️: say it plainly, propose the fix (smaller steps or
a re-plan step) and APPLY the recommended one — naming it in the
brief — never a menu of alternatives for the operator. "Bis zum
Self-Run" = count of unchecked STATUS lines from the current position
through F075 inclusive. Capability lines: "kann jetzt" only for
merged, verified behavior (P1).
--- END phv4-r1-3 ---

--- BEGIN phv4-r1-4 sha256=19e3f85fe382eac1c6ad99e5369bd5e6e4f1682e111ae5ae9c77de66cc6aa2d2 ---
Flake-debt visibility: whenever an integration gate attributes more than
10 branch-only failures to the pre-existing flake class, the
"Läuft's rund?" cell must name the growing flake debt and recommend
reopening flake work via F252 follow-ups. The reviewer registers the
recommended reorder as a DECISION per §4 item 7 — loud, persisted,
reversible by any later relay — never as a question to the operator.
--- END phv4-r1-4 ---

--- BEGIN phv4-r1-5 sha256=b63db559086c5c1dc9deaeb83cc46337c6a55748cc95ad52bef91418fc39bc2d ---
7. A wrong spec is a finding routed to planning — the reviewer authors
   the concrete feature-file amendment INTO the current paste block,
   records it as an operator-visible DECISION (chosen option,
   alternatives considered, how to reverse) in the brief and the
   ledger, and proceeds under the recommended option. The operator's
   veto is any later relay; nothing waits for an answer. Never
   silently re-plan: the decision is loud, persisted, and reversible,
   just not a question.
--- END phv4-r1-5 ---

--- BEGIN phv4-r1-6 sha256=f6644e33d53ce96411b5fe4a258b89e34139225cd2ebb48e72db7d810af41399 ---
12. Before diagnosing a relay gap ("the block never reached the
    worker"), read .agent/last_block.md and its git history. A
    recorded refusal means delivered-and-refused: re-emit CORRECTED
    bytes, never the same bytes, and never conclude "never delivered"
    while a refusal record exists (PH v3 lesson: three refused
    emissions left zero disk trace and the gap was misdiagnosed for
    three turns).
--- END phv4-r1-6 ---

--- BEGIN phv4-r1-7 sha256=8ae895f213897a18a4b9cb36b244fe7d961164180ebff10e103325f80351b610 ---
On ANY refusal or duplicate STOP (refused-hash-gate /
stopped-duplicate), the worker COMMITS AND PUSHES
`.agent/last_block.md` — OUTCOME line set accordingly, plus one
evidence line (expected vs computed hash, or the duplicate's commit
shas) — as the round's only commit. A refusal that leaves no disk
trace is itself a handback defect. (This clarifies "committed with
the round bookkeeping" for rounds where the bookkeeping commit IS the
refusal.)
--- END phv4-r1-7 ---

--- BEGIN phv4-r1-8 sha256=fc5f709ca70dd09131e049bb5974dccd1e8530b478b63b2433750bc89ff977e7 ---
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
--- END phv4-r1-8 ---

--- BEGIN phv4-r1-9 sha256=eb5327a73d2ef7c1172854b51f77d2c19a56d328e54ced6565bf6d6143ec7768 ---
- A STOP or refusal reply contains: the banner, the evidence line(s),
  and nothing else. It never assigns tasks, questions, or
  instructions to the operator — remediation requests travel to
  Window 1 via .agent/last_block.md and the handback on disk. The
  operator relays; the operator is never the addressee of technical
  work.
--- END phv4-r1-9 ---

--- BEGIN phv4-r1-10 sha256=ec70ff73159ef76356872dfd9cfc9165b12f1de14a47194b78454afc5ab89eeb ---
# Live Review — Process-hardening v4 (decide-and-proceed + refusal visibility)

Branch: chore/process-hardening-v4
Scope: docs/agents/planner_reviewer_prompt.md and
docs/agents/split_workflow.md — docs-only amendments (four operator
rulings: separator redesign, refusal disk-trace, decide-and-proceed,
worker STOP etiquette).

## Steps
- R1: apply authored texts phv4-r1-1..11, run gates, hand back.

## Findings
(none)

## Verdicts
(reviewer-authored only)
--- END phv4-r1-10 ---

--- BEGIN phv4-r1-11 sha256=d55de1e80d8cdeec6eafbee02927e949767e6dac6301fa6b0bef0dd7f6354dcb ---
# Plan — PH v4 process-amendment round (before F252)

## Goal
Persist four operator-accepted process rulings as docs-only
amendments to docs/agents/planner_reviewer_prompt.md and
docs/agents/split_workflow.md; reviewer-gated; operator-approved
same-session merge on PASS.

## Next Steps
- R1: worker applies authored texts phv4-r1-1..11, verifies
  (containment + cmp + contract tests + canary + tests/docs), pushes,
  hands back.
- Reviewer verdict; on PASS merge the PR; F252 starts in a fresh
  session.
--- END phv4-r1-11 ---

