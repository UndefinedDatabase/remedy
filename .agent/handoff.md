# Handback — F083 R25 (session-closing persistence round)

## Range
Review of 94ceafa2..HEAD on feature/f083-ci-self-check — 5 commits, `.agent/` only.
Open findings: 104 (116 registered, 12 resolved, 0 landed). Next free id R-0489.

## Commits
### 8203a58d docs(f083): save the R25 step block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f083-r25.md | +161/-0 | C0a: block saved verbatim, sha256 21dbf26e…7724cd, 14465 B, 161 lines |
### 1b101bd4 chore(agent): mirror the R25 block into last_block
| Path | +/- | Reason |
|---|---|---|
| .agent/last_block.md | +79/-150 | C0b: mirror of the COMMITTED authored file |
### 05e0cf4d docs(review): record the R24 PASS verdict
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +4/-0 | C1: RECORD-R24 EOF-append, nothing edited |
### 0ccf1986 docs(f083): advance the plan past R24
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +9/-9 | C2: PLAN slice, whole file |
### (this commit) docs(agent): rewrite the handback for R25
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | C3: this file; a handoff cannot table its own commit |

## External actions
`git push -u origin feature/f083-ci-self-check` after C3; result in the round report. No PR created, none merged. No worktree added or removed.

## Verification — ordered item-status table, measured
| Item | Status | Measured |
|---|---|---|
| 1 pwd / clean / worktree / STOP | done | /home/decodeux/Repos/remedy; `git status --porcelain` empty at round start and before C3; `git worktree list` 1 line at both; `.agent/STOP` absent at both |
| 2 base HEAD | done | 94ceafa2c8dfb061a49f5799d9d756cb7ab13941 = 94ceafa2 |
| 3 authored = last_block | done | committed blobs byte-equal; both sha256 21dbf26eeaec7c0a…, 14465 B, 161 lines |
| 4 C1 pure append | done | 300239 B prefixes 305119 B; 4880-B tail byte-equals the extracted RECORD-R24 slice; `git show --numstat` `4 0`; BEGIN-marker LINES 0 at base and 0 at HEAD, substring `BEGIN SLICE` 4 and 4 |
| 5 plan.md = PLAN slice | done | byte-equal; sha256 ff88ab851c0cb6d8…; 39 lines (<50); `## Goal` and `## Next Steps` present; 0 unchecked-box lines |
| 6 `ONE TEST` count | done | 0 in docs/system/ci-self-check-v1.md |
| 7 range gate | done | `git diff --name-only 94ceafa2..HEAD -- docs/ packages/ apps/ scripts/ tests/` printed nothing, exit 0 |
| 8 ruff, taken at C2 0ccf1986 | done | `Found 26 errors.` / `[*] 25 fixable`, exit 1 — ratchet unchanged |
| 9 verification set + canary | done | `78 passed in 31.54s`, exit 0 |
| 10 tests/docs | done | `295 passed in 0.30s`, exit 0 |
| 11 open set at HEAD | done | 116 registered, 12 resolved, 0 landed, 104 open; max R-0488, next free R-0489; 0 duplicate ids, 0 unregistered resolutions; R-0488 resolved, R-0482 and R-0487 open |
| 12 change set | done | exactly `.agent/authored/f083-r25.md`, `.agent/handoff.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md` — nothing else |
| 13 per-commit insertions, linear | done | 161, 79, 4, 9 for C0a–C2 plus this commit's own state-file rewrite, none near 500; single-parent chain 0ccf1986←05e0cf4d←1b101bd4←8203a58d←94ceafa2; reflog shows only `commit:` entries, no amend, rebase or reset |

## Authored-text proofs
`.agent/authored/f083-r25.md` is byte-identical to the transported block and to the ordered
digest: sha256 21dbf26eeaec7c0aee97ea5e216c23286c71631f0cddaae88e13ab39847724cd, 14465 B,
161 lines. Both slices were extracted programmatically from the COMMITTED authored file by
their markers; neither target file contains a marker line.

## Deviations & assumptions
The block's ordered commit sequence C0a, C0b, C1, C2, C3 was followed exactly: five
commits, none added, none dropped, none reordered.
- C0b reading discrepancy, declared, not a defect: `git commit`'s rewrite summary
  printed `161 insertions(+), 232 deletions(-)` while `git show --numstat` gives
  `79 150`. Gate 13 uses numstat. Both are far under 500, and the commit is an exempt
  single `.agent/**` state-file rewrite under the AGENTS.md counting rule.
- Nothing outside `.agent/` was touched; the 26 ruff errors stand, ceiling not raised.
- Stated-cause overage (DECISION D15): this file is 70 lines against the 60-line cap.
  Cause is mandated content only: five per-commit tables at 4 lines each and a 13-row
  item-status table. No section dropped, no transcript padded.

## Next
1. Read `.agent/STOP` from disk before anything else.
2. Run the AGENTS.md Open PR Gate.
3. Then the integration-gate round per docs/agents/integration_gate.md — full suite once, branch plus a base run in a throwaway worktree.
