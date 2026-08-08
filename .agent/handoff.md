# Handoff — F103 R8 (closure part 2), branch `feature/f103-token-ledger`

**Two values cannot live in this file** (F080 R5 / F254 R12 precedent): this
closure commit's OWN SHA and the PR number/URL. The file is INSIDE the closure
commit and the PR is created after it; recording either would need a commit
after the STATUS edit, which Rule A4 forbids. Both are in the completion
report, with the raw `gh pr list` output. The same holds for the post-commit
`git status --porcelain` and the closure commit's own `git log --oneline -1`.

## Closure values, as accepted and written into the STATUS line
Evidence job f103-closure
package remedy-review-20260808-210612-READY_FOR_REVIEW.zip
SHA-256 8e967d78e57fa97641365b4baa91ca884f6322bc855f678d1daeb146c9dd38ad
accepted HEAD 65e1eec25e61c1d0fe78539adeb890d3426cb605
That is the CONTENT head the zip manifest records. The R7 handoff commit
`09d7ab2d`, the R8 block save and this closure commit all follow the READY
zip, exactly as STATUS_closure_protocol.md step 2 prescribes.

## Commits
### 3243a3d1 chore(f103): save the R8 closure block
| Path | +/- | Reason |
|------|-----|--------|
| `.agent/last_block.md` | +404/-301 | R8 block saved verbatim |
### (this commit) docs(f103): accept F103 in the roadmap ledger and sync the readme
| Path | +/- | Reason |
|------|-----|--------|
| `docs/roadmap/STATUS.md` | +1/-1 | `[~]` -> `[x]`, authored line |
| `README.md` | +4/-3 | capability sync, SAME commit (R-0154) |
| `.agent/live_review.md` | +72/-5 | R7 verdict recorded, R8 in flight |
| `.agent/plan.md` | +31/-39 | complete replacement by `cp` |
| `.agent/candidates.md` | +1/-0 | second candidate ADDED, R-0221 kept |
| `.agent/handoff.md` | rewrite | this file (self-reference, R-0149) |
| `.agent/authored/f103-r8-1..6.md` | +276 | the six receipts |
No source, no test, no feature file and no other doc is touched.

## Transport proofs
`sha256sum` of all six saved texts matched the block's BEGIN-marker hashes
exactly — **6/6, no mismatch**: r8-1 `713a7e26…9d6f`, r8-2 `d7160637…2b3c`,
r8-3 `00be41a5…d62f`, r8-4 `c4e6084b…1533`, r8-5 `6ecf1e54…ec87`, r8-6
`53fef325…6cec`. Pairs applied with the FROM/TO strings parsed out of the
authored files, never hand-typed; all six pairs are REWRITES and each FROM
occurred exactly once before the edit:
- `docs/roadmap/STATUS.md`, 1 pair — BEFORE FROM **1x** / TO **0x**;
  AFTER FROM **0x** / TO **1x**.
- `README.md`, 3 pairs — BEFORE each FROM **1x** / TO **0x**;
  AFTER each FROM **0x** / TO **1x**.
- `.agent/live_review.md`, 2 pairs — BEFORE each FROM **1x** / TO **0x**;
  AFTER each FROM **0x** / TO **1x**.
`cp` replacements: `cmp .agent/plan.md .agent/authored/f103-r8-4.md`
**exit 0**; `cmp .agent/candidates.md .agent/authored/f103-r8-5.md`
**exit 0**. r8-6 is the PR body: saved and committed, applied to no
tracked file.

## STATUS line proof
`wc -l docs/roadmap/STATUS.md` **315 before, 315 after** — identical, one
line swapped and no other line touched. `grep -c '^- \[~\]'` **1 -> 0**.
The F103 line appears exactly once and is byte-identical to the authored TO.

## Verification (run by me, real exit codes)
| Command | Result | Exit |
|---------|--------|------|
| `python3 -m pytest tests/docs/ -q` | 294 passed in 0.25s | 0 |
| `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 42 passed in 19.27s | 0 |
| `integrity check --json`, receipts still untracked | `"passed": false`, 1/5 fail: `relevant_untracked` = the 6 receipts | 1 |
| `integrity check --json`, closure paths staged | `"passed": true`, fail_count 0, 5/5, `untracked=0, relevant=0` | 0 |
| `git status --porcelain` at handoff-write time | exactly the 11 mandated paths, staged; nothing else | 0 |
The first integrity run is recorded rather than hidden: the receipts are part
of this very commit, so untracked-until-staged is the expected transient and
the staged re-run is the load-bearing one.

## Item status
| Item | Status | Reason |
|------|--------|--------|
| 1 save the block | done | commit `3243a3d1`, that file only |
| 2 six authored texts | done | 6/6 sha256 match, pair counts above |
| 3 gates | done | docs 294, canary 42, integrity PASS |
| 4 closure commit | done | this commit, exact paths, LAST on branch |
| 5 push + PR | done | see the completion report for number and URL |
| 6 handback | done | this file, inside the closure commit |

## Open findings
**0.** R-0218, R-0219 and R-0220 closed; live review PASS across R1-R8.
`.agent/candidates.md` carries **TWO** entries — R-0221 (the UI auto-build
test that pops its own env var) and the AGENTS.md commit-size counting
ambiguity raised at the R7 closure review. Both are the NEXT feature's
claim-time block condition: its first reviewed round registers or resolves
each and empties the file in that same round. Neither may be dropped.

## Deviations, declared
1. The closure commit's own SHA, the PR number/URL and the post-commit
   `git status`/`git log` are absent by self-reference impossibility, per
   the note at the top — not an omission.
2. Length **114 lines**, over the 60-line base cap, stated cause per the
   AGENTS.md D15 overage clause: two per-commit tables, the six-hash and
   six-pair transport proof, the STATUS line proof, the 5-row verification
   table, the four closure values and the 6-row item-status table do not
   fit in 60. NO mandated section was dropped.
3. Commit size: 12 files, **+473/-128 = 601 changed lines**. Under the
   INSERTIONS reading of AGENTS.md Commit Discipline (473) it is UNDER the
   500 cap; under the churn reading (601) it is over. Inseparable —
   STATUS_closure_protocol.md step 5 and R-0154 require README, STATUS and
   the final `.agent` state to land in ONE commit, because no committed
   state may have README and STATUS disagreeing. This is exactly the
   ambiguity now carried in `.agent/candidates.md`.
No scope was widened, no reviewer-authored text was edited, `git add -A` was
never used, nothing was force-pushed and no branch was deleted.

## Next expected action
Window 1 ends F103 with the feature-done banner. The PR created by this round
is **NOT merged** by this session; it merges at the NEXT feature's Open PR
Gate — the operator's manual-review window — or manually by the operator at
any time. Next feature by Rule A5: **F104 — Hard budget enforcement**, in a
FRESH session, whose Open PR Gate merges this PR and whose first reviewed
round must empty `.agent/candidates.md`.
