# Handoff — F107 Context compiler v2, round R22

Branch: feature/f107-context-compiler-v2 (base 56ee7dc1, R21 gated on its four
committed items).
Fortschritt: ~98 % (T001-T004 ✅ · Integration Gate ✅ · Built State ✅ · Evidence + Zip ✅ · STATUS-Zeile + PR offen) — Schätzung

Deviations, declared: this handoff is 125 lines, over the 60-line cap, per
AGENTS.md DECISION D15. Cause: the mandated content — the C1-C6 SHA list, the
changed-files table, the item-status table, the seven gate results A-G with
their real output, and the six closure values — does not fit in 60. No section
is dropped.

## Commits (all pushed, one push per commit)
| Item | SHA      | Subject                                                       |
|------|----------|---------------------------------------------------------------|
| C1   | 70a96ca6 | chore(f107): save the R22 step block verbatim                  |
| C2   | e79f8689 | chore(f107): mirror the R22 block into last block              |
| C3   | 16723f88 | chore(f107): register R-0297, a block ordering an unreachable path |
| C4   | b823dff9 | chore(f107): amend DECISION F107 D3 with a reachable archive path |
| C5   | (none)   | artifacts only — nothing committed, nothing deleted            |
| C6   | (this)   | chore(f107): rewrite the plan and handoff for R22              |

## Changed files (56ee7dc1..HEAD), `git show --numstat` per commit
| Path                          | Commit | +   | -   |
|-------------------------------|--------|-----|-----|
| .agent/authored/f107-r22-1.md | C1     | 251 | 0   |
| .agent/last_block.md          | C2     | 149 | 173 |
| .agent/live_review.md         | C3     | 21  | 1   |
| .agent/decisions.md           | C4     | 35  | 0   |
| .agent/plan.md                | C6     | see C6 diff |
| .agent/handoff.md             | C6     | see C6 diff |

## Item status
| Item | Status | Reason |
|------|--------|--------|
| C1   | done   |        |
| C2   | done   |        |
| C3   | done   |        |
| C4   | done   |        |
| C5   | done   | all 7 sub-steps ran; every `mv` succeeded, nothing deleted |
| C6   | done   |        |

## Gates — real results
A transport: `cmp .remedy-wt/f107-r22-1.block.md .agent/authored/f107-r22-1.md`
  no output, exit 0. `wc -l` = 251. `sha256sum` =
  234b2749b9d39df425196af09477a5e30543ff295db741993e74017e01060630, identical
  for the scratch original. `cmp .agent/authored/f107-r22-1.md
  .agent/last_block.md` no output, exit 0.
B block cap: GREEN. 251 lines against the cap of 400 (DECISION F105 D5).
C pairs, in .agent/live_review.md after C3 (16723f88) — all five counts hit:
  `^> Branch:.*Next free ID: R-0297` 0 · `...R-0298` 1 · `^- R-0297` 1 ·
  `^Done:` 13 (unchanged) · `^Landed:` 0.
  `git show --numstat 16723f88 -- .agent/live_review.md` = `21 1`.
  Shapes: PAIR_HDR is the one REWRITE — its FROM is 0x and its TO 1x in the
  file. PAIR_LRF is APPEND-shaped and proved as such: its three-line FROM still
  occurs exactly 1x in the file, and each of its 20 non-blank TO-only lines
  occurs exactly 1x among the 21 lines C3's own diff adds. 20 + 1 header = 21.
  Added lines belonging to no TO body = 0.
D decisions: `grep -c '^## DECISION F107 D3a' .agent/decisions.md` = 1 ·
  anchor `neither the move nor this decision is needed again.` still 1x ·
  `^## DECISION F107 D3 ` still 1 (the original is NOT edited) · the bytes
  directly after the anchor are `\n## DECISION F107 D3a (2026-08-12) — …`, so
  the payload's first non-blank line directly follows it.
  `git show --numstat b823dff9 -- .agent/decisions.md` = `35 0`, zero deletions.
E marker leak: `^<<<` = 0 in .agent/live_review.md, .agent/decisions.md,
  .agent/plan.md and .agent/handoff.md. Pre-existing backtick-quoted `` `^<<<` ``
  strings inside seven finding bodies are mid-line, not line-anchored, and the
  gate is line-anchored — noted so a future reader does not read them as a leak.
F artifacts:
  Archive (D3a), all three `mv` exit 0, NOTHING deleted:
    .remedy-wt/.cache/f107-archive/r11gate · …/r9gate · …/f107_closure_evidence_r20
    …/rejected-remedy-review-20260812-232923.zip (35071672 bytes)
    `.remedy-wt/` no longer holds r9gate, r11gate or f107_closure_evidence.
  Refreshed run lines, each exit 0, 0 failed and 0 skipped:
    vr0001 tests/orchestration/test_context_compiler.py          -> 65 passed in 0.18s
    vr0002 test_context_compiler_e2e.py + test_job_context_cmd.py -> 15 passed in 2.85s
    vr0003 tests/docs/                                            -> 294 passed in 0.32s
    vr0004 tests/cli/test_golden_path.py                          -> 42 passed in 21.20s
  Evidence bundle: job id f107-closure · head b823dff9 · total_passed 416 ·
    authority_count 12 · commit_count 126 · final verifier verdict
    PASS_WITH_RISKS.
  Package: remedy-review-20260812-235227-READY_FOR_REVIEW.zip · script exit 0 ·
    package_status READY_FOR_REVIEW · review_subject_alignment PASS ·
    sha256 computed by the worker
    4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d,
    identical to the script's reported final_sha256 · 15730864 bytes.
  Package opened and counted by the worker: member_count 4096 · members matching
    the packager's own `:509` rejection regex 0 · members under
    `.remedy-wt/.cache` 0, so the D3a prune held · local-path leaks (`:516`) 0.
    For contrast, R20's rejected package was 10534 members with 1834 unsafe.
    `.remedy-wt/*` members 1652 — swept in but all safe; the durable prune fix
    R-0295 names is still owed to the packager's own follow-up.
  Manifest `.review_zip_manifest.json` committed_review_subject: base
    2e4142c3ac72042ac4d704da252db263e48dcba3 (as required, base_is_ancestor
    true) · head b823dff9b4711ec3cc3505b496589cd02e219fc4.
    Stated: that head is C4, the HEAD at build time — C5 builds before C6 by the
    block's own ordering, so the plan/handoff commit lands after the package.
G tree, push and scope: `git status --porcelain` empty · `git worktree list` the
  primary checkout alone · `git rev-list --left-right --count
  origin/feature/f107-context-compiler-v2...HEAD` = `0 0` after the last push ·
  `git diff --name-only 56ee7dc1..HEAD` = exactly the six `.agent/` paths the
  Change line names and nothing else · insertions per commit 251, 149, 21, 35
  and the C6 pair, each far under 500 · `gh pr list --state open` = `[]`.

## Closure values
1. Evidence job id: f107-closure
2. Package filename: remedy-review-20260812-235227-READY_FOR_REVIEW.zip
3. Package SHA-256: 4497c8e1bdb54ac3a0c5069dffcb9184303ceaa85f6c075ba81c09a14927ff8d
4. Final verifier verdict: PASS_WITH_RISKS
5. Full-suite counts, BOTH runs at head ca8e36ab, never collapsed (R-0296):
   R20 worker's run:  5 failed, 16537 passed, 19 skipped in 143.59s
   Reviewer's run:    6 failed, 16536 passed, 19 skipped in 143.86s
6. Integrity check: ok true, failures [], notes [] (manifest_integrity.json).

## Findings
Registered `^- R-0` = 35; resolved `^Done: R-0` = 13; derived open = 22. This
round registered R-0297 and resolved nothing, so open rose from 21 to 22.
Next free ID: R-0298. None above Medium.

## Next expected action
Reviewer gate on R22, then R23 — the closure commit: the reviewer-authored
STATUS `[x]` line, the README capability sync in the SAME commit (R-0154), the
final `.agent/` state, then the PR. Verdict PASS_WITH_RISKS for the five
pre-existing R-0286 `[reviewer]` failures plus the R-0296 flake. No gate is RED
this round.
