# Handback — F033 · SESSION 5 CLOSE · rounds 17 through 20

> Written by the REVIEWER at the close of session 5 and applied by a worker,
> because the reviewer writes no work-tree file itself. It carries the round 20
> verdict and one reviewer prose slip. Operator amendment amend0827 rule 1: a
> verdict committed and pushed HERE is persisted, and is booked into
> `.agent/live_review.md` in the FIRST COMMIT of the next round that is happening
> anyway — never in a round of its own.

## Session

SESSION 5 of feature F033 · rounds 17, 18, 19 and 20 delegated · rounds so far 20.
The NEXT session is SESSION 6 of 7 against the amend0827 rule 6 soft limit.
THE SOFT LIMIT IS CLOSE AND SESSION 6 MUST PLAN FOR IT: 20 rounds of 25, 5
sessions of 7. Whichever arrives first triggers the scope report, and on the
current shape 25 arrives first. See "The soft limit" below.

## Fortschritt

~95 % (T001 and T002 complete. T003: the partial-apply truth now renders on ALL
THREE surfaces and R-0738 is RESOLVED; the rejection→repair renderer exists and
is proved verbatim. What remains: wiring that renderer into the next builder
round, the two-round end-to-end, R-0745, and the closure sequence with its
`docs/` obligation and integration gate) — Schätzung.

## Range

`d526dfb5`..`203689cf071ba7f8e7d8358cf641427e5f8822d5` on branch
`feature/f033-hunk-approval-v2`, pushed; `origin/feature/f033-hunk-approval-v2`
is at the same commit. Session 5 alone added 39 commits over
`5f0273d8`..`203689cf`. Every round was gated by the reviewer, which re-ran each
round's own gates from scripts of its own, reproduced every ordered reading, and
re-ran every mutation with its own anchors in its own disposable worktree before
writing a verdict.

## Verdicts

| Round | Subject | Verdict | Ledger entry |
|-------|---------|---------|--------------|
| 17 | the tasks-card row learns the partial apply state | PASS | `Gate: F033 R17` at `440de7ea` |
| 18 | the apply fold gets a shared home and its counts | PASS | `Gate: F033 R18` at `e057697d` |
| 19 | the report line, R-0738's third surface | PASS | `Gate: F033 R19` at `d9db68ef` |
| 20 | rejected hunks as verbatim repair findings | PASS | NOT YET BOOKED — see below |

## Round 20 verdict — PASS, and it is not yet in the ledger

The next round books it. Every gate was re-executed by the reviewer at
`203689cf`. TRANSPORT: `cmp` of the committed `.agent/authored/f033-r20.md`
against the reviewer's OWN scratchpad original, SILENT — one end of that
comparison is the reviewer's file rather than the worker's. Each slice region
was read AT THE COMMIT THAT APPLIED IT and is byte-EQUAL to its original:
PLAN20 at `69084af5` (2570 bytes over 46 lines), RECORD20 at `d9db68ef` (10101
bytes), SLIPS20 at `688cf561` (1622 bytes). THE RECORD APPEND reconstructs
1565456 plus one newline plus 10101 to 1575558, base a byte PREFIX, slice an
exact SUFFIX, N COUNTED at 3 over 713 blank-line units, and a negative control
at byte 1568181 — proved to lie inside the FIRST appended paragraph, spanning
1565457 to 1570905, exactly the span the block stated — REJECTED by both readers
run independently, each of which accepted the unflipped file. THE LEDGER:
registered 307 UNMOVED; `Done:` 50 lines over 48 distinct to 52 over 50 with the
ADDED ids exactly `R-0738` and `R-0746`; `Landed:` 18 UNMOVED with the
`Landed: R-0746` line still standing beside its new `Done:` paragraph, which is
this branch's append-only precedent; `^Gate: F033 R19 — ` 0 before and exactly 1
after; distinct `DECISION F033 D` ids 5 UNMOVED; and the open set 259 to 257 —
the first time this feature's open set has FALLEN. THE PROSE FILES:
`.agent/prose_slips.md` reconstructs 28040 plus one newline plus 1622 to 29663.
THE MODULE IS PURE AS ORDERED and its docstring documents both deliberate
absences — it renders nothing that was approved, and it has no caller yet. THE
VERBATIM RULE HOLDS WHERE IT MATTERS: `entry.reason` is appended raw, never
stripped, wrapped, escaped or indented, and the reason is deliberately NOT put
through the coercion guard, because rendering the string "None" where an
operator's words belong would put words in their mouth. THE MUTATIONS were
re-run by the reviewer in its own disposable worktree at `203689cf` with its OWN
anchors, each asserted UNIQUE, the file restored and PROVED byte-identical
against the committed blob: unmutated control 17 passed at REAL exit 0; dropping
the reason is exit 1 at 8 failed; rendering non-rejected entries is exit 1 at 3
failed; and removing the STRUCTURAL guard is exit 1 at 5 failed. THE REVIEWER
ALSO RAN A FOURTH MUTATION THE BLOCK NEVER ORDERED, to settle the worker's own
deviation D4 rather than take it on trust: removing ONLY the coercion guard
`_total_text`, leaving the structural guard intact, reddens EXACTLY ONE test —
`test_an_id_whose_str_raises_returns_rather_than_raises` — which is precisely
the one the structural mutation left green. The two guards are therefore
measured by DISJOINT tests, 5 and 1 covering all six totality assertions, and
the worker's design decision is confirmed correct. THE SUITES were re-run
SERIALLY in the primary checkout, every REAL exit 0: the new file 17, the hunk
ledger 29, hunk approval 30, `test_named_bugs.py` 64 passed and 6 skipped,
`test_resource_safety.py` 21, and the canary 42, with `ruff` exiting 0 over both
new files. THE STRUCTURE: nine single-parent commits over
`d4a21259`..`203689cf` of 344, 238, 20, 6, 6, 130, 294, 294 and 17 insertions,
every one under 500; the path set over the WHOLE range EQUALS the declared
change set in BOTH directions; and all sixteen do-not-touch paths blob-identical
at both ends.

## The worker's nine deviations — all honest, and one is the reviewer's own error

D4 IS A DEFECT IN THE REVIEWER'S BLOCK AND THE WORKER WAS RIGHT TO RESOLVE IT
RATHER THAN APPLY IT NAIVELY. SPEC A6 ordered totality on all inputs, a
re-stated coercion guard, AND empty-string-on-unreadable. Written the obvious
way those are two overlapping defensive layers, and gate G6(iii) — "remove the
totality guard so a broken input raises" — would then have reddened NOTHING,
because the surviving layer answers every case. The block never said which guard
is the guard. The worker made the structural guard singular and load-bearing,
confined the coercion guard to the hunk id, documented the split in the module,
and ran a fourth mutation of its own to show both are measured. The reviewer
reproduced that fourth mutation independently and confirms it. Recorded as a
prose slip below.

D3 deserves a note for its honesty rather than for any fault: the worker used
`git worktree remove --force` and stated it had NOT first tried without the flag,
so it could not claim the flag was necessary. That is the correct way to report
an unmeasured choice.

D1, D2, D5, D6, D7, D8 and D9 need no action: `ruff` ran as `python3 -m ruff`
because the sandbox denies the bare executable; the extra mutation is the one
above; a reason is never coerced, which is right; the ordered AST guard cannot
see module-level CONSTANTS so the worker added a second test that does; the
standing constraint the block cited is already on disk in `.agent/context.md`
and that path was outside the change set; no `Done:` or `Landed:` line of the
worker's own was written and `Landed: R-0746` was not deleted; and the new
module has no caller, by design.

## Reviewer prose slip — for `.agent/prose_slips.md`, no id, no round of its own

2026-08-29 · F033 R20 · The block's SPEC A6 ordered totality on all inputs, a re-stated coercion guard AND empty-string-on-unreadable without saying which of those is THE guard, so the obvious reading produces two overlapping defensive layers and the block's own G6(iii) would have reddened nothing — a mutation defeated by redundancy rather than by a missing test; the worker made the structural guard singular, confined the coercion guard to the id, and proved both are measured by disjoint tests, and a SPEC ordering defence in depth must name which layer its red-proof is aimed at.

## What this session built

| Path | What it decides | Tests |
|------|-----------------|-------|
| `apps/ui/src/components/panels/TaskChecklistCard.tsx` | the task row's partial tile and status text | 20 |
| `apps/ui/src/components/panels/RightLivePanel.module.css` | the blue filled check tile `ux_spec.md` 11.4 binds | — |
| `packages/orchestration/proof_chain.py` | the apply fold's shared home, and its APPLIED/TOTAL counts | 104 |
| `packages/orchestration/run_report.py` | the report's task line, R-0738's third surface | 81 |
| `packages/orchestration/hunk_repair_findings.py` | rejected hunks as repair findings, reasons verbatim | 17 |

R-0738 (Medium) and R-0746 (Low) were RESOLVED this session; R-0746 was also
raised in it. DECISION F033 D5 was ruled. The open set went 258 to 257 — it FELL
for the first time on this feature.

## The soft limit — session 6 must plan against it

Operator amendment amend0827 rule 6 sets the soft limit at 25 ROUNDS or 7
SESSIONS, whichever comes FIRST. This feature stands at 20 rounds and 5
sessions, so 25 rounds arrives first and there are FIVE rounds of headroom. The
remaining work, as the plan carries it, is: the renderer's wiring into the next
builder round, the two-round end-to-end the Acceptance asks for, R-0745, the
`docs/` operator description, the integration-gate round, and the closure
sequence. That is five to six rounds against five of headroom, so session 6
should expect either to finish exactly at the limit or to owe the scope report.
It is NOT owed yet and no scope report is written here; this paragraph exists so
session 6 plans with the count in front of it rather than discovering it.

## Next expected action — SESSION 6, in this order

1. Read `.agent/STOP` from disk. If it exists, hand off and end (Phase 1 rule 1
   before rule 2 — finding R-0347).
2. Run the Open PR Gate. There was no open PR at the close of session 5 and this
   session created none: F033 is not closed, and §5 rules the PR into the
   closure sequence.
3. The next round's FIRST commits book, into `.agent/live_review.md`, the round
   20 verdict above, and append the prose slip above to `.agent/prose_slips.md`.
   Neither buys a round of its own.
4. Then the round's real work: WIRE `render_rejection_findings` INTO THE NEXT
   BUILDER ROUND'S PROMPT. Measured by the reviewer at `203689cf`:
   `packages/orchestration/hunk_repair_findings.py` has NO caller, by design;
   `packages/orchestration/repair_context.py` builds a repair context from a
   FAILED TEST RUN and is not the seam for a rejection, so do not assume it is;
   and the feature file's Design says rejections reuse "steering-style volatile
   injection", which means the injection point must be located in the builder's
   prompt path before anything is written. THIS ROUND NEEDS ITS OWN GROUND
   READING and the reviewer did not spend it in session 5.
5. Then the two-round end-to-end the Acceptance asks for: the same hunk id
   returning in round two carries its prior rejection reason.
6. R-0745 is open and belongs with the next work touching the door's imports;
   its FIX clause names two routes and recommends the transitive-closure test.
7. The closure sequence still owes `docs/` an operator-facing description of
   `remedy patch approve-hunks`. No round has been allowed a `docs/` path yet,
   and the plan carries it as an explicit item so it is not discovered at
   closure. The integration gate runs before closure, per
   docs/agents/integration_gate.md.
