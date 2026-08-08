# Handback — F254 R12, closure part 2 — FEATURE CLOSED

Feature **T2_F254 — model alias table & dead-model doctor check**, branch
**`feature/f254-model-alias-table`**. SPLIT round, worker subagent.
`.agent/STOP` absent at round start and re-checked before the commit.

**Two values cannot live in this file** (F080 R5 precedent): the closure
commit's own SHA and the PR number. This file is INSIDE the closure commit,
so it cannot name that commit's hash, and the PR is created after it. Both
are in the completion report. Recording them here would require a commit
after the STATUS edit, which Rule A4 forbids.

## THE FOUR CLOSURE VALUES (as written into the STATUS line)
- Evidence job id: **`f254-closure`**
- Package: **`remedy-review-20260807-204305-READY_FOR_REVIEW.zip`**
- SHA-256: **`1b4995fa9e3ab76f7be8398be66ed69ec47e99f6e825d16cc97aa826a95a05c0`**
- Accepted HEAD: **`b71c9bdd93cbeb21d4b98842cdf6baa998c3ac26`** — the last
  CONTENT commit, which is what the manifest records. The R11 handoff commit
  `38a909c6` and this closure commit follow the READY zip, exactly as
  STATUS_closure_protocol.md step 2 prescribes.

## Changed files — the ONE closure commit (`38a909c6..HEAD`)
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS.md | +1/-1 | authored `[x] F254` line: job, package, SHA-256, accepted HEAD |
| README.md | +5/-2 | capability sync: 39 of 255 accepted; Tier 2 at 1 of 14; Tier 2 item named |
| .agent/live_review.md | +75/-13 | authored R11 PASS verdict + the R12 CLOSURE entry |
| .agent/plan.md | +34/-38 | authored replacement — F254 CLOSED, F103 next |
| .agent/authored/f254-r12-{1,2,3,4}.md | new | the four receipts, byte-identical copies |
| .agent/handoff.md | rewrite | this handback |
Exactly the R-0154 path set — nothing else. STATUS and README land in the
SAME commit, so no committed state has them disagreeing. The feature file's
Built State was already current from `d8294663`. Staged by exact path;
`git add -A` was not used. `.agent/context.md` and `.agent/decisions.md` were
deliberately NOT touched: they are outside this round's mandated path set.

## Transport and pair proof (PRIMARY evidence)
All four receipts `cp`-copied, never hand-typed. `cmp` against the reviewer's
scratchpad originals **exit 0 x4**; `sha256sum` matches the authored block for
all four. `cmp .agent/plan.md .agent/authored/f254-r12-2.md` **exit 0**.
Six pairs, each under its DECLARED shape:
- r12-1 → live_review.md, PAIR 1+2 REWRITE: pre FROM **1x** → post FROM **0x**, TO **1x**.
- r12-3 → STATUS.md, PAIR 1 REWRITE: pre FROM **1x** → post FROM **0x**, TO **1x**.
- r12-4 → README.md, PAIR 1+2 REWRITE: pre **1x** → post FROM **0x**, TO **1x**;
  PAIR 3 APPEND: FROM **1x** before AND after, each TO-ONLY line **1x** after.
STATUS.md line count **315 before, 315 after** — unchanged, one line swapped.
`grep -c '^- \[x\] F'` **38 → 39**; README now reads `39 of 255`, so the two
agree in the committed state.

## Verification (real commands, real exit codes, before the commit)
    python3 -m pytest tests/docs/ -q                    -> 0 · 294 passed in 0.26s
    round gate (dashboard+test_runner+resource_safety)  -> 0 · 142 passed in 18.40s
    python3 -m pytest tests/cli/test_golden_path.py -q  -> 0 · 42 passed in 18.86s
`tests/docs/` is the pin that catches a README/STATUS disagreement; green
means they agree in this exact state. `remedy integrity check --json` ran
twice: BEFORE the commit `passed false`, fail_count 1 — the only failing
check `relevant_untracked` naming the four not-yet-committed receipts, which
the commit itself resolves; AFTER the commit `passed true`, 5/5 pass. No red
verification was left standing; the STOP rule never fired.

## Findings
R-0211…R-0217 all Done. **Open findings: 0. Next free ID: R-0218.**
`.agent/candidates.md` still holds the R-0214 handoff-cap amendment — a BLOCK
CONDITION at the NEXT feature claim, not at this closure.

## Deviations, declared
1. Closure commit SHA and PR number absent, per the note at the top — a
   self-reference impossibility, not an omission.
2. This file is 82 lines, over the 60-line cap, with NO section dropped —
   R-0214's ninth measurement, caused by the four closure values, the
   six-pair proof and the self-reference note.
No scope was widened; no reviewer-authored text was edited; the PR is NOT
merged by this round.

## Next expected action
Window 1 ends F254 with the feature-done banner. The closure PR merges at the
NEXT feature's Open PR Gate — the operator's manual-review window; the
operator may merge it manually at any time instead. Next feature: **F103 —
Token ledger (SQLite)**, which Rule A5 names. Its first reviewed round MUST
register or resolve the R-0214 entry in `.agent/candidates.md` and empty the
file in that same round; a non-empty candidates file is a block condition at
feature-claim time.
