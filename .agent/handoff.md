# Handback — R0154 micro-round R1 (closure protocol v4) — DONE

## Range
Review of 757e06f..HEAD · feature/r0154-closure-ordering · docs-only ·
Open PR Gate cleared (#161 merged) · one commit · PR #162 open, NOT merged.

## Commits
### 16458e2 docs(closure): codify the R-0154 ordering lesson — closure protocol v4
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/STATUS_closure_protocol.md | +12/-6 | FULL REPLACE with authored v4: header v3→v4; step 5 pins the R-0154 ordering (README sync in the SAME commit as the STATUS `[x]` edit; closure commit touches exactly STATUS.md, README.md, final .agent/ state) |
| .agent/live_review.md | rewrite | R0154 micro-round review; `## Verdicts` left `(pending R1)` — worker wrote no verdict |
| .agent/plan.md | rewrite | R0154 micro-round plan |
| .agent/last_block.md | rewrite | R1 block guard + the three authored texts verbatim |
| .agent/authored/r0154-r1-{1,2,3}.md | +new | the authored sources, sha256-verified before any apply |

## External actions
`gh pr merge 161 --merge --delete-branch` (Open PR Gate, exit 0); 1 push to
origin/feature/r0154-closure-ordering; `gh pr create` → **PR #162**. NOT merged.
No worktree.

## Verification
- Open PR Gate: `gh pr list --state open --json number,headRefName,baseRefName,isDraft`
  → exactly one — `{"baseRefName":"main","headRefName":"feature/f252-standing-red-paydown","isDraft":false,"number":161}`.
  Merged (exit 0), fast-forward 7baff1d..757e06f, branch deleted. `git checkout main
  && git pull --ff-only` → "Already up to date."
- Docs gate: `python3 -m pytest tests/docs/ -q` → exit **0**, tail: `292 passed in 0.31s`.
- Canary: `python3 -m pytest tests/cli/test_golden_path.py -q` → exit **0**, tail:
  `42 passed in 14.94s`.
  Both match the F252 baseline (292 / 42).
- Diff review: `git diff docs/roadmap/STATUS_closure_protocol.md` = exactly two hunks
  (v3→v4 header, step 5 rewrite). No other file outside the block's Change list.

## Authored-text proofs
On-disk `sha256sum` matched the BEGIN markers BEFORE any apply — all three:

    d2b67cb5d12254aa9ed7253287eae8aa6a8895c83b000d7746b41c45df0545f9  .agent/authored/r0154-r1-1.md
    e3066d09858a8687175f8ec0477a18ef549f9380d3d4aabaf72aff8dfb541f34  .agent/authored/r0154-r1-2.md
    f87463160259b1b1cfedf89a593fcf10eb37502827d4892ab70a31cffaeb7046  .agent/authored/r0154-r1-3.md

Applied by copy; `cmp` authored vs target → exit **0**, all three. Post-apply
`sha256sum` of the three targets equals the same three digests.

## Deviations & assumptions
- **Transport wrap on r0154-r1-1 (recovered, verified).** As first saved, the text
  hashed `07f21848…`, not `d2b67cb5…`. Cause: the step-4 STATUS-line template had been
  hard-wrapped in transport, split after `· package`. Rejoining the two fragments with a
  single space reproduced the authored bytes exactly. Confirmed independently: the v3
  file on disk carries that same template as one unwrapped line, and the resulting diff
  shows no change to it. Nothing was applied while the hash mismatched; the trial ran in
  the scratchpad. Recorded in `.agent/last_block.md` as TRANSPORT NOTE.
- **Two commits, not one.** Step 7's single commit carries the whole Change list. The
  round-end state — `OUTCOME: pending` → `executed` (step 3) and this handoff rewrite
  (Handback line) — can only be written after the PR exists, so it lands in a second,
  mechanical commit. Alternative would have been handing back with a dirty tree.
- Commit message carries no `Co-Authored-By` trailer, matching every prior commit in
  this repo.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 Open PR Gate (#161) | done | |
| 2 branch | done | |
| 3 last_block guard | done | flip to `executed` in the round-end commit |
| 4 authored texts + sha256 | done | r0154-r1-1 needed wrap recovery — see Deviations |
| 5 apply by copy + cmp | done | 3 × exit 0 |
| 6 docs gate + canary | done | 292 / 42, both exit 0 |
| 7 one commit + push | deviated | round-end state needed a second commit — see Deviations |
| 8 PR (not merged) | done | #162 |
| 9 handback | done | this file |

## Next
Reviewer R1 review of PR #162 → writes `## Verdicts` in `.agent/live_review.md`.
On PASS: merge #162 (operator pre-authorized), then bootstrap F050 — DAG scheduling.
