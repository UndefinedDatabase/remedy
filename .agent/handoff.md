# Handoff — F111 Diff-only repair · Round 22 (CLOSURE)

Branch: feature/f111-diff-only-repair · base 4e0b762e · start HEAD 35329dec
Next expected action: Window 1 gates this round. The closure PR is created and
left UNMERGED by design; it merges at the next feature's start (Open PR Gate).

Deviations, declared — 71 lines, because DECISION D15's mandated content
(item-status table, commit table, changed-files table, the a-m gate block with
real values, the closure artefact values) does not fit smaller. No section
dropped. Two self-reference limits: C6 cannot name its own SHA or its own
insertion count, and the PR number does not exist until after C6. All three are
in the handback report as measured values.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1a | done | |
| C1b | done | |
| C2  | done | |
| C3  | done | |
| C4  | deviated | bundle #1 rejected at zip time (unsorted `test_files`); rebuilt clean |
| C5  | deviated | zip #1 BLOCKED_EVIDENCE + unsafe-member abort; zip #2 READY_FOR_REVIEW |
| C6  | done | this commit |
| C7  | done | pushed, PR created, NOT merged |

## Commits (35329dec..HEAD)
| SHA | Subject | Ins |
|-----|---------|-----|
| 591612f2 | chore(f111): save the R22 step block verbatim | 325 |
| d5a960d6 | chore(f111): mirror the R22 block into last_block | 292 |
| 6e15240d | chore(f111): record the R21 integration gate and resolve R-0319 | 67 |
| a2fe520b | docs(f111): record the shipped shape in the feature file | 18 |
| (this commit) | chore(f111): close F111 in the ledger | self-count impossible |

## Changed files
| Path | Commit |
|------|--------|
| .agent/authored/f111-r22-1.md | C1a |
| .agent/last_block.md | C1b |
| .agent/live_review.md | C2 |
| docs/roadmap/features/T2_F111.md | C3 |
| docs/roadmap/STATUS.md · README.md · .agent/plan.md · .agent/candidates.md · .agent/handoff.md | C6 |

## Gates (real values)
a `cmp` exit 0 · sha256 both 881ef3573142d211a872e0457a6d2830bf91fd50864a7d0f126768a4b5a00fc8 · `wc -lc` 325 20472
b Done: 13 · Landed: 0 · `### R21 — PASS` 1 · `- R-0` 44
c R19 slice = 32 lines · `are byte-identical` 0 · `WERE byte-identical` 1
d tests/docs/ `294 passed in 0.30s`, exit 0 · grep diff-only-repair-v1.md = 1
e `integrity check --json` passed=true, fail_count=0, check_count=5, relevant untracked 0
f Evidence job `f111-closure` · verdict PASS_WITH_RISKS · 85 scoped node ids, 85 passed
g package remedy-review-20260813-060242-READY_FOR_REVIEW.zip · SHA-256
  c44b4a12a5715a66bf3abd55633fc86a77351b0018fab930f374e707458d79e6 · subject
  4e0b762e48cf29672eee979f74c282b10136f59c..a2fe520bd16773e4f1536035caeec76e880bbdde
h applied STATUS line == authored TEXT-D outside the 3 slots, proved both directions ·
  `- [x] F111 — ` 1 · `- [~]` 0
i `- [x] Fxxx — ` 44 · README "44 of 255 registered items accepted." · same commit
j tests/docs/ `294 passed in 0.26s` exit 0 · golden path `42 passed in 19.58s` exit 0
k `wc -l .agent/plan.md` = 42 (cap 50)
l tree clean · 35329dec..HEAD = the 9 ordered paths, no evidence dir, no zip · 0/0 vs origin
m PR created against main from this branch, open, not draft, NOT merged (number in report)

## Artefact attempts (AGENTS.md rule)
1. bundle #1 + zip #1 — FAILED: `remedy-review-20260813-060103-BLOCKED_EVIDENCE.zip`,
   validation error `verification_tests.json runs[0] test_files is not sorted`, and
   REVIEW_ZIP_ERROR unsafe members from stale scratch `.remedy-wt/f111r11/dg/.git`.
2. bundle #2 + zip #2 — READY_FOR_REVIEW, values in (f) and (g).

Open findings: 32 (44 registered − 12 resolved). None High; each an accepted risk.

Fortschritt: 100 % (T001 ✅ · T002 ✅ · T003 ✅ · Doku ✅ ·
Integration Gate ✅ · Closure ✅) — Schätzung
