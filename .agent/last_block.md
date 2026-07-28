OUTCOME: pending
── STEP PH-v3/1 — process-hardening v3 (relay ergonomics) — FORMAT-UPDATE RE-EMISSION ──
Note:        Supersedes the two refused unfenced emissions AND the
             fenced one you may hold but have not executed (no phv3
             effects on disk). r1-1 is UPDATED again (operator dropped
             the bottom delimiter: top separator only, block runs to
             the end of the reply) — new hash below. r1-4/r1-5 carry
             your third guard case as before; r1-2/3/6/7/8 unchanged.
             Bytes differ from anything you refused — proceed.
Goal:        Persist the five PH v3 operator rulings (2026-07-28) into
             the process docs; docs only; PR created, merged only after
             the reviewer's PASS (operator-approved same-session merge).
Bundle:      Open PR Gate (#158) → chore branch → Commit A bookkeeping →
             B planner prompt → C split_workflow → D handback template →
             verify → push → PR → handback.
Change:      ONLY: .agent/authored/phv3-r1-*.md, .agent/live_review.md,
             .agent/plan.md, .agent/last_block.md (new),
             docs/agents/planner_reviewer_prompt.md,
             docs/agents/split_workflow.md,
             docs/agents/handback_template.md, .agent/handoff.md.
Constraints: AGENTS.md wins on conflict — STOP and surface. Authored
             texts via .agent/authored/ with sha256 check BEFORE commit;
             wrap → join + re-verify; residual mismatch → STOP with
             received bytes. Commits <500 lines.

(procedure steps 1-7 and Done/Handback as received; authored texts follow verbatim)

--- BEGIN phv3-r1-1 sha256=a308e164a969cafe387e45c8e23c8e083538a07402ae246498356a1585457837 ---
**Paste-block format (PH v3, operator ruling 2026-07-28):** the paste
block is ALWAYS the LAST content of the reply — nothing after it,
ever; recaps and notes go before it. The ENTIRE block is emitted
inside a fenced code block so no markdown renderer on the relay path
can mutate its bytes (PH v3 lesson: an unfenced emission had heading
markers, blockquote markers and leading indentation stripped in
transit — every authored hash in it broke). ONE separator line marks
the top:
──────── PASTE BLOCK — COPY FROM THE NEXT LINE TO THE END ────────
There is NO bottom delimiter: the block ends where the reply ends
(the closing fence), which is unambiguous because nothing may follow
the block. SEPARATOR LINE ONLY — never side borders or per-line
prefixes: any character added to a content line becomes part of the
copied bytes and breaks every sha256 in the block. Authored texts
appear ONLY inside that single block, exactly once per reply;
rendering an authored text or the block region twice in one reply is
a defect of the reply, treated like a transport fault (F251-R3
lesson: a duplicated, truncated render broke an authored hash
unrecoverably).
--- END phv3-r1-1 ---

--- BEGIN phv3-r1-2 sha256=770a0b7f55346c0e7b1176499e6540b4d3f39d19684115dcac36afa4f775d6c8 ---
  5. **Docs-round gate (PH v3, operator ruling 2026-07-28):** any
     round whose change set includes docs/roadmap/** gates with
     `python3 -m pytest tests/docs/ -q` in addition to the canary;
     a ledger-count change and its test pin land in the SAME commit
     (R-0151 — the F251 registration broke the feature-ledger pins
     because its gate was canary-only).
--- END phv3-r1-2 ---

--- BEGIN phv3-r1-3 sha256=079fb749787050ed6b5780747eab602597261060901831c2f09237032436795d ---
11. Authored `.agent` state texts satisfy the repo's own `.agent`
    contract tests (PH v3): every authored `.agent/live_review.md`
    reset/replacement carries a `## Steps` section (the tests assert
    the substring "Steps"), and every authored `.agent/plan.md` text
    keeps `## Goal` plus a `## Next Steps` heading — so
    reviewer-authored state never turns contract tests red as a side
    effect (F251 D4 lesson: authored texts flipped four contract
    tests in both directions across rounds). The D4 design question
    itself — fixture-based vs live-coupled — stays with F252.
--- END phv3-r1-3 ---

--- BEGIN phv3-r1-4 sha256=7d64e779249fac713ad81ba64fd11b476a68cdb178ad1a12003895f6474ffc2c ---
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
--- END phv3-r1-4 ---

--- BEGIN phv3-r1-5 sha256=e74d6304bff313993abd6578a8d188d8e62d9c5479592078fcd674b16e7dac2f ---
- FIRST bookkeeping action of every round: write .agent/last_block.md
  (overwrite): line 1 `OUTCOME: pending`, then the received paste
  block VERBATIM; update OUTCOME at round end (executed /
  refused-hash-gate / stopped-duplicate). If the received block is
  byte-identical to the stored one: previous OUTCOME executed → STOP,
  reply `##### SAME PROMPT AGAIN — PROBABLY A RELAY MISTAKE #####` +
  one evidence line; previous OUTCOME refused-hash-gate → STOP
  likewise (a loop — the same bytes cannot pass the gate), never
  re-run the failed check; no record / relay gap → deliberate
  re-issue: proceed and note it in the handback.
--- END phv3-r1-5 ---

--- BEGIN phv3-r1-6 sha256=736f098860f02bcd78dbbf76baff0540a3bfc40a836efd34ef2bf40b522a81ee ---
> Write-once rule (PH v3): draft the handback in the session
> scratchpad, measure it there (`wc -l`) against the cap, then write
> and commit `.agent/handoff.md` ONCE — trim commits against the cap
> are a smell, not a workflow (F251 lesson: 116→91→110→103→100).
--- END phv3-r1-6 ---

--- BEGIN phv3-r1-7 sha256=e22f40334e93077a6c87a33c50bf901043c6dda12c44c7f51bad53592af9b268 ---
# Live Review — Process-hardening v3 (relay ergonomics)

Branch: chore/process-hardening-v3 (PR at close)
LAST_REVIEWED_SHA: main head at branch creation (recorded in handoff)
Finding IDs continue monotonically; next free ID: R-0154.
Previous ledgers (F251, planning amendment, F048) live in git history.

## Steps

- R1: apply the five PH v3 doc changes (authored texts phv3-r1-1..6),
  verify, hand back. Reviewer review + PASS → same-session merge
  (operator-approved, PH v1/v2 precedent).

## Findings

(none this round)

## Verdicts

(pending)
--- END phv3-r1-7 ---

--- BEGIN phv3-r1-8 sha256=3ff59e3b01ee284618360cfaa1c92f786e380aca332f89ba56586c521b281482 ---
# Plan — Process-hardening v3 (relay ergonomics, R1)

## Goal
Persist the five PH v3 operator rulings (2026-07-28) into the process
docs: planner paste-block output format, worker duplicate-block guard
(.agent/last_block.md), docs-round gate for docs/roadmap/** changes,
handback write-once rule, and the authored-state contract rule
(## Steps in live_review, ## Goal + ## Next Steps in plan). Docs only.

## Next Steps

- [ ] Open PR Gate: merge PR #158 (F251), main pulled clean
- [ ] Branch chore/process-hardening-v3
- [ ] Commit A: authored files + live_review (phv3-r1-7) + this plan
      (phv3-r1-8) + .agent/last_block.md written (first use of the
      new guard, self-applied)
- [ ] Commit B: planner_reviewer_prompt.md — §2 paste-block format
      (r1-1), §3 docs-round gate (r1-2), §4 authored-state contract
      rule (r1-3)
- [ ] Commit C: split_workflow.md — duplicate-block guard (r1-4) +
      worker bootstrap bullet (r1-5)
- [ ] Commit D: handback_template.md — write-once rule (r1-6)
- [ ] Verify: containment proofs; the four .agent contract tests
      green (live_review + plan now carry the required substrings);
      canary; docs-only diff
- [ ] Push, PR into main (NOT merged until the reviewer's PASS),
      handback per template — drafted in scratchpad, written once

## Risks
- Docs only: any non-docs diff besides .agent/ bookkeeping is scope
  drift — stop and report.
- AGENTS.md wins on any conflict — STOP and surface, never weaken.
--- END phv3-r1-8 ---

