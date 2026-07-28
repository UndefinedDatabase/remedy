# Handback — PH v4: four process rulings persisted (docs only)

## Range
Review of `bcc7ede..HEAD` — `chore/process-hardening-v4`, 4 commits, pushed, PR open, NOT merged.

## Commits
### 38c6065 bookkeeping · 0982b01 planner · ecbf95f split_workflow · this commit
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/phv4-r1-1..11.md | +134 | 38c6065 — eleven texts, sha256-verified |
| .agent/last_block.md | +164 −58 | 38c6065 — OUTCOME pending + received block |
| .agent/{live_review,plan}.md | +19 −58 | 38c6065 — full replaces r1-10 / r1-11 (cmp 0) |
| docs/agents/planner_reviewer_prompt.md | +40 −18 | 0982b01 — r1-1..r1-6 (5 replaces, 1 insert) |
| docs/agents/split_workflow.md | +19 −1 | ecbf95f — r1-7 append, r1-8 replace, r1-9 insert |
| .agent/{last_block,handoff}.md | this commit | OUTCOME→executed; this handback (R-0149 self-ref) |

## Item status
| Item | Status | Reason |
|---|---|---|
| Open PR Gate | done | `gh pr list --state open` → empty; main bcc7ede clean |
| 1 Commit A | done | 38c6065; 11/11 sha256 matched first try |
| 2/3 Commits B,C | done | 0982b01 (6 edits), ecbf95f (3); containment 0 ×9, absence 0 ×3 |
| 4 verification a–g | done | 4d/4f pre-existing red only — see below |
| 5/6 Commit D + PR | done | this commit; PR created, NOT merged |

## External actions
`gh pr list --state open` → `[]` (raw: no output) · branch from bcc7ede · push per commit · `gh pr create` → PR open, NOT merged. No merges this round.

## Verification
    4a containment exit 0 ×9 — r1-1..6 planner_reviewer_prompt, r1-7..9 split_workflow
    4b cmp exit 0 — r1-10 vs live_review.md, r1-11 vs plan.md
    4c grep -c = 0 ×3 retired strings ("COPY FROM THE NEXT LINE TO THE END",
       "needing an operator decision", "F135/F052 flake debt")
    4d test_dashboard_contract.py -q → 2 failed, 68 passed
    4e canary test_golden_path.py -q → 42 passed · 4f tests/docs/ -q → 13 failed,
       279 passed · 4g git status --porcelain → empty

**4d/4f are NOT regressions — proven, not asserted.** The 15 failing ids diffed
against the catalogued F251 baseline (`churn_gate2_run1.txt`): `comm -23` EMPTY,
so all are pre-existing standing red owned by F252. The 13 in tests/docs are
README pinned-text drift; the 2 in dashboard_contract read `.agent/context.md`,
untouched by this round.

## Authored-text proofs
All eleven matched their BEGIN markers on the FIRST attempt (no recovery needed):
`a9229592… 4716a3d3… bd284198… 19e3f85f… b63db559… f6644e33… 8ae895f2… fc5f709c…
eb5327a7… ec70ff73… d55de1e8…`

## Deviations & assumptions
- Duplicate-block guard: previous `.agent/last_block.md` carried `OUTCOME:
  executed` and these are new bytes → normal execution, as the rule prescribes.
- Gap worth a ruling: the PH v3 authored-state rule (§4 item 11) covers
  `live_review.md` and `plan.md` but NOT `.agent/context.md`, still F046's and
  keeping two contract tests red. r1-10/r1-11 satisfy the four tests the rule
  names; the context.md pair stays red, with F252.
- The local `chore/process-hardening-v3` ref still exists (remote deleted on
  merge); outside this round's change set. Open findings: 0; no AGENTS.md conflict.

## Next
Handing back to Window 1 for review of bcc7ede..HEAD.
