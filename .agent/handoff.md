# Handback — F086 R31 (closure)

## Range

Review of d1889132..HEAD — 5 commits, C0a C0b C1 C2 C3, one worker; C3 is the closure commit and, per Rule A4, the last commit on the branch.

## Commits

| # | SHA | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 6a690bd3 | .agent/authored/f086-r31.md | 373/0 | save the R31 block |
| C0b | ff959aa1 | .agent/last_block.md | 296/330 | mirror the block |
| C1 | e453d9af | .agent/plan.md | 22/25 | PLAN31 — plan advanced to R31 |
| C2 | 4ce7f204 | .agent/live_review.md | 4/0 | FIND0597 registered, RECORD30 appended |
| C3 | self | docs/roadmap/STATUS.md | 1/1 | STATUSLINE — `[~]` becomes `[x]` |
| C3 | self | README.md | 4/3 | RMCOUNT, RMTIER, RMLIST — the capability sync |
| C3 | self | .agent/handoff.md | 32/34 | this handback (R-0149 self-reference) |

| Item | Status | Reason |
|---|---|---|
| Bundle 1 — block saved and mirrored | done | C0a + C0b, byte-equal |
| Bundle 2 — plan advanced to R31 | done | C1, first substantive commit (§3 item 23) |
| Bundle 3 — FIND0597 and RECORD30 | done | C2 |
| Bundle 4 — closure commit, three paths TOGETHER | done | C3; the README sync may not split from the `[x]` line (R-0154) |
| Bundle 5 — pull request, created and NOT merged | done | run after C3; number and URL in the round report, never in this file |

## External actions

The branch push, `gh pr create --base main --head feature/f086-release-capability --title "F086 Release capability — closure" --body-file .remedy-wt/f086_pr_body.md` and the `gh pr list` re-read all run AFTER C3 and therefore cannot appear in a file that C3 contains — constraint 6; their real output is in the round report. The PR is NOT merged by this session: it merges at the next feature's start through the AGENTS.md Open PR Gate, the operator's manual-review window. No worktree was added or removed; no other `gh` command ran.

## Verification

- G1 HYGIENE — `.agent/STOP` read from disk before C0a and again here, absent both times; branch feature/f086-release-capability; `git status --porcelain` EMPTY after every commit and here; `git worktree list` 1 line throughout; no primary-checkout file was overwritten to take a reading — every non-current reading came from `git show <sha>:<path>`.
- G2 TRANSPORT — `.remedy-wt/f086-r31.md`, the committed C0a and the committed C0b are byte-EQUAL at sha256 832e466af3e5afa5a726adacfbc0cb2d2289f118329cd8072baf6bf8799663bc, 27551 B over 373 lines; that digest is the one the reviewer stated before delegating.
- G3 PLAN — `.agent/plan.md` at C1 byte-equals PLAN31 extracted programmatically from the committed C0a: sha256 4dec604a1eccd08d5cdab08559c822fac1b1224b95a041b5b4abc782c95471f7, 41 lines (under the 50-line cap), with `## Goal`, `## Next Steps` and `F086` all present.
- G4 LEDGER APPEND — the pre-C2 blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder equals a blank line, FIND0597, a blank line and RECORD30, at sha256 25f0c89475f053a5522904acff6e045bb65e147ce998f60206410e8b2fd8d69b; both blank separators are present (R-0578).
- G5 LEDGER SETS — two independent extractions AGREE at both ends: 179 registered / 6 resolved / 0 dup / 0 unregistered / 0 `Landed:` / 173 open at d1889132, and 180 / 6 / 0 / 0 / 0 / 174 at C2. The registered set gains EXACTLY `R-0597` and loses none; the resolved set is UNCHANGED, so no resolution is unregistered at any point. The CONTROL over f0b27118..7b84524c MOVES: `[]` registered gained, exactly `R-0584` resolved gained.
- G6 ITEM-20 SCAN — backtick-quoted spans deleted first, then `\bHEAD\b` reads 0 over C2's 4 added lines; the RED CONTROL, the same extractor over fd166295's 4 added lines to the same file, reads 3.
- G7 ITEM-26 HEADERS — 27 headers at d1889132 and 28 at C2; the set occurring more than once is UNCHANGED and exactly `Gate: R19 — the R18 entry.`; `Gate: R31 — the R30 entry.` occurs 1x, is the LAST such header, and the text following it begins `R30 ` once its leading space is stripped.
- G8 THE STATUS LINE — `TO contains FROM: False`, so a REWRITE: STATUSLINEFROM occurs 1x at d1889132 and 0x at C3, STATUSLINETO 1x at C3, and the ORDERED EQUALITY holds — the C3 file equals the d1889132 blob with that single occurrence replaced and nothing else changed. sha256 a7e037ca31f89a1d246ca664b0a3a74e429fc08aa5a9fa1c443f903afa7065b5, 342 lines against the base's 342. In that file `- [x] F086 — Release capability (` occurs 1x and `- [~] F086` 0x, and the `[x]` line carries each of the four closure values exactly 1x: `f086-closure`, `remedy-review-20260820-200318-READY_FOR_REVIEW.zip`, `bc140179628e8698ef2bd7354cfb30187554f277312f524c9d6ab0324b500855`, `f5fa19c368ed15d14ee6067fc69fde4fbc7863a6`.
- G9 THE README SYNC — three pairs, each with its own containment reading: RMCOUNT `TO contains FROM: False`, RMTIER `False`, RMLIST `False` — all three REWRITES, RMLIST included, because its TO ends the F107 entry with a comma where the FROM ends it with a period. Each FROM occurs 1x at d1889132 and 0x at C3, each TO 1x at C3, and the ORDERED EQUALITY over the whole file holds. sha256 eba9521187a0db95996399b753d32774bc8b093158b00fa7be28782d26d72ba7, 125 lines against the base's 124.
- G10 THE LEDGER CROSS-CHECK — serially in the PRIMARY checkout, no second pytest process at any point: `python3 -m pytest tests/docs/ -q -rf` exit 0, `295 passed in 0.52s`, beside the 295 measured at d1889132 — the accepted-id cross-check, the accepted-COUNT pin and the tier-table Done pin all read the numerals this round wrote. Then `python3 -m pytest tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_contract.py tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py -q -rf` exit 0, `160 passed in 19.98s`; then the canary `python3 -m pytest tests/cli/test_golden_path.py -q` exit 0, `42 passed in 20.43s`.
- G11 RULE A4 AND THE PATH SET — C3 stages EXACTLY `docs/roadmap/STATUS.md`, `README.md` and `.agent/handoff.md`: three paths, no more and no fewer, and no fourth path is modified or untracked in the tree. C3 is authored as the branch terminator; the committed `git diff --name-only C3^ C3` and the proof that no commit follows C3 are in the round report, because a file inside C3 cannot read C3.
- G12 NO MARKER LEAKED — LINES beginning `<<<SLICE ` or `<<<END ` count 0 in `.agent/plan.md` at C1, `.agent/live_review.md` at C2, and `docs/roadmap/STATUS.md` and `README.md` as staged for C3.
- G13 CHANGE SET, HISTORY AND THE HANDBACK — the range path set over d1889132..HEAD equals the Change list with no path on either side alone; all eight paths the Change section forbids are PRESENT at d1889132 and untouched, and nothing under `apps/`, `packages/` or `tests/` was touched; the range is linear (one parent each) and every `git reflog` entry of this round is `commit:`. Every `+/-` cell above is pasted from `git diff --numstat <sha>^ <sha>`, max insertion column 373 under the 500 cap. This file is 58 lines against the 60-line bound constraint 11 states, with all seven mandated headings of docs/agents/handback_template.md present in the template's order.
- G14 THE PULL REQUEST — ordered LAST and run after C3, so no reading of it can exist in this file; the push, the `gh pr create`, the resulting number and URL, and the literal `gh pr list --state open --json number,headRefName,baseRefName,isDraft` re-read are all in the round report. It is not merged.

## Authored-text proofs

PLAN31, FIND0597, RECORD30, STATUSLINE FROM/TO, RMCOUNT FROM/TO, RMTIER FROM/TO, RMLIST FROM/TO and PRBODY were extracted PROGRAMMATICALLY from the committed C0a at 6a690bd3 — never retyped, rewrapped or summarised — and applied byte-verbatim; G3, G4, G8 and G9 carry the disk-to-disk digests and the per-pair containment readings. No marker line reached any target, and PRBODY was written to `.remedy-wt/f086_pr_body.md` for `--body-file` rather than composed.

## Deviations & assumptions

None. The commit sequence was C0a, C0b, C1, C2, C3 exactly as the block labels it — nothing added, dropped or reordered — and no slice was edited, so no constraint-1 declaration was needed this round. Assumption, stated because it is load-bearing: the four closure values are quoted from the block's Goal, which records R30's measurements; this round re-derived none of them and the review package was neither rebuilt nor moved.

## Next

The reviewer reviews d1889132..HEAD, re-runs every gate, and records R31's verdict. R31 is the branch terminator, so that verdict lives in this file, in the PR and in the reviewer's report rather than in a later ledger entry (§4 item 13's carve-out for the round whose bundle CREATES the PR). The pull request is open and must NOT be merged by this session; it merges at the next feature's start through the Open PR Gate. The next feature is selected by Rule A5 as the first `[ ]` in `docs/roadmap/STATUS.md` — F255 — in a FRESH session, whose first reviewed round reads `.agent/candidates.md`, which this closure leaves empty and correct.
