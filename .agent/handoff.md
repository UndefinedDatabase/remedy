# Handback — F086 R17, record R16 and repair R-0584 (branch feature/f086-release-capability)

## Range

Review of 4750383c..HEAD

## Commits

| # | Commit | Path | +/- | Reason |
|---|---|---|---|---|
| C0a | 8a320ffc | .agent/authored/f086-r17.md | +414/-0 | the R17 block, byte-verbatim |
| C0b | 44e8843a | .agent/last_block.md | +259/-335 | mirror of the COMMITTED C0a |
| C1 | 3a29cc10 | .agent/plan.md | +13/-10 | the PLAN17 slice, whole file |
| C2 | 6d1a7e73 | .agent/live_review.md | +4/-0 | FIND0584 then RECORD15, appended |
| C3 | 3bedad72 | tests/orchestration/test_release_workflow.py | +3/-3 | the three FROM/TO pairs |
| C4 | 0dfc945b | .agent/live_review.md | +2/-0 | the one `Landed: R-0584 —` line |
| C5, C6 | this commit and the next | .agent/handoff.md | rewrite, then +44 | R-0149: cannot table itself; C6 appends VERDICT |

## External actions

`git worktree add --detach .remedy-wt/r17-mut 0dfc945b` and `git worktree add --detach .remedy-wt/r17-base 4750383c` for G9's six runs, then `git worktree remove --force` on each plus `git worktree prune`; `git worktree list` now reads one line. `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`; no PR created, no branch created, nothing merged. `git push -u origin feature/f086-release-capability` runs after C6 and the round report carries its outcome.

## Verification

G1 primary tree porcelain EMPTY at every commit and at the handback; `.agent/STOP` absent, re-read from disk before C0a and again at the handback; branch `feature/f086-release-capability`, HEAD at 4750383c when the round began.
G2 `.remedy-wt/f086-r17.md` ≡ the committed authored file ≡ the committed last_block, all three byte-EQUAL at sha256 5edb6fb56580f0060a3506944ce49969060bcc000335180f5d26418364d6c620, 29930 B over 414 lines; re-measured from the COMMITTED file the block is 414 total / 294 prose / 120 slice incl. 20 marker lines — what constraint 6 declares of itself.
G3 `.agent/plan.md` ≡ PLAN17 at sha256 610d15f861e2b47a83e8b53a6c30ffa7f037e05506c5b6fcaff386a7e9b25c85, 46 lines (under 50), holding `## Goal`, `## Next Steps` and `F086`.
G4 the pre-C2 ledger blob is a byte-exact PREFIX of the post-C2 blob whose 4-line remainder ≡ FIND0584 followed by RECORD15 at sha256 c7ac0e52078092e599cd225db6dde0b9544e5f6933206c1127c37fcf26e97bc1; the post-C2 blob is in turn a byte-exact PREFIX of the post-C4 blob, whose remainder is one blank line plus exactly one line, verbatim: Landed: R-0584 — the three positive release-workflow guards now assert over `executable_lines()` instead of `workflow_text()`, so a comment can no longer satisfy them; committed as 3bedad72.
G5 HEAD reads 167 registered / 2 resolved / 0 duplicate ids / 0 unregistered resolutions / 1 `Landed:` line / 165 open under BOTH extractions, and the two registered SETS are EQUAL; the symmetric difference of the HEAD registered set against the 4750383c set is exactly `['R-0584']`, and the same extractor over 6f5a589a..efc021d9 reads `['R-0583']`, so that reading is a difference the extractor can see.
G6 0 lines beginning `<<<SLICE ` or `<<<END ` in `.agent/plan.md`, `.agent/live_review.md` and `tests/orchestration/test_release_workflow.py` at HEAD; `.agent/handoff.md` can only be counted after C6 and that reading is in the round report.
G7 in `tests/orchestration/test_release_workflow.py`, each FROM is 1x and each TO 0x at 4750383c and each FROM 0x and each TO 1x at HEAD — six counts before, six after; the base blob with each FROM occurrence replaced by its TO is byte-EQUAL to the file at HEAD, `git diff --numstat` reads 3 insertions and 3 deletions, and the file is sha256 72db2e02767e95b8813c684ee5be5d63de4c43aaea2fcaf28101b39377d0b3bf over 70 lines, unchanged from 70.
G8 exit 0, 28 passed — the workflow guards, the gate-wiring suite and the gate suite together, primary checkout.
G9 six runs, one mutation at a time, each fully reverted before the next, in two disposable worktrees — MUT at 0dfc945b and BASE at 4750383c, each target line counted 1x in that worktree's `.github/workflows/release.yml` before it was written: (a) dropping the `missing` fallback from the `conclusion=` echo → MUT exit 1, 1 failed / 6 passed naming ONLY `test_release_workflow_refuses_when_no_ci_run_is_found`, BASE exit 0, 7 passed; (b) commenting out the sole `workflow_dispatch:` line → MUT exit 1, 1 failed / 6 passed naming ONLY `test_release_workflow_is_triggered_by_hand_only`, BASE exit 0, 7 passed; (c) interpolating the tag into the runner's shell line → MUT exit 1 and BASE exit 1, each 1 failed / 6 passed naming ONLY `test_release_workflow_passes_the_tag_through_the_environment`. After the last revert each worktree re-ran at exit 0, 7 passed with its own `git status --porcelain` EMPTY, and each revert was byte-exact against the pre-mutation bytes.
G10 ruff over `tests/orchestration/test_release_workflow.py`, the round's only Python path: at 4750383c read in the disposable BASE worktree, exit 0 with an EMPTY rule-code multiset, and at HEAD in the primary checkout, exit 0 with an EMPTY rule-code multiset — the two multisets are EQUAL.
G11 exit 0, 160 passed for the four state readers, then exit 0, 42 passed for the canary. They did NOT overlap: the second process was launched only after the first had ENDED and reported its exit code.
G12 linear, every commit exactly one parent: 4750383c → 8a320ffc → 44e8843a → 3a29cc10 → 6d1a7e73 → 3bedad72 → 0dfc945b; `git reflog` over this round shows only `commit:` entries — no amend, rebase, reset or force-push. Insertions before C5, from the `+` column of `git show --numstat`: 414, 259, 13, 4, 3, 2 — none over 500, and no DECISION F104 D1 exemption invoked.
G13 `git diff --name-only 4750383c..HEAD` before C5 is exactly the five paths tabled above other than `.agent/handoff.md`. All seven other paths constraint 2 forbids — `.github/workflows/release.yml`, `scripts/release_gate_check.py`, `packages/orchestration/release_gate.py`, `pyproject.toml`, `hatch_build.py`, `.github/workflows/ci.yml` and `CHANGELOG.md` — EXIST at 4750383c under `git ls-tree`, so the prohibition forbids something real, and nothing under `apps/` or `docs/` is in the range.
G14 this file is 56 lines as C5 writes it and C6 appends the 44-line VERDICT slice, so the file at HEAD is 100 lines — AT MOST 100, with NO DECISION D15 overage declared — and all seven mandated headings of docs/agents/handback_template.md are present, in the template's order. The post-C6 `wc -l` reading is in the round report.
G15 C6 appends VERDICT by pure concatenation, nothing else in this file changing; the prefix-and-remainder equality against the blob C5 committed can only be measured after C6, so that measurement is in the round report.
G16 `gh pr list --state open --json number,headRefName,baseRefName,isDraft` → `[]`. Nothing created, nothing merged.

## Authored-text proofs

PLAN17, FIND0584, RECORD15, the six PAIR slices and VERDICT were each extracted programmatically by their one-line `<<<SLICE NAME>>>` / `<<<END NAME>>>` markers from the COMMITTED `.agent/authored/f086-r17.md` and applied byte-verbatim; none was retyped, reformatted or edited, and no marker line reached a target file. Each applied region byte-EQUALS its slice, verified disk-to-disk against the committed blob. Every sha256 is written out in full, at 64 characters, above and in the round report; none is written anywhere in part.

## Deviations & assumptions

- ORDERED COMMIT SEQUENCE: no deviation. C0a, C0b, C1, C2, C3, C4, C5, C6 ran in the block's order, one commit each, none extra, none dropped, none reordered.
- The Verification section above is a per-gate SUMMARY, not the raw transcript this template's wording asks for. The block's step 6 orders that as the R-0582 repair; the full transcript lives in the round report, which no cap binds, and no section is dropped. FINAL length of this file: 56 lines from C5 plus the VERDICT slice's 44 = 100.
- `Range` names the literal token `HEAD`, the R10-onward convention on this branch: a handoff cannot name the SHA of the commit that writes it. The only text the worker authored into a tracked file this round is C4's single `Landed:` line; FIND0584, RECORD15 and the appended session verdict are the REVIEWER's own text, applied byte-verbatim, and the worker wrote no verdict anywhere.

## Next

1. Re-read `.agent/STOP` from disk (Phase 1 rule 1).
2. Run the Open PR Gate (Phase 1 rule 2): `gh pr list --state open --json number,headRefName,baseRefName,isDraft`.
3. Then review `4750383c..HEAD` and record R17's verdict in `.agent/live_review.md` (Phase 1 rule 4).
