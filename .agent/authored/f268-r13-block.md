-- STEP R13 closure round B -- F268 remedy do: the one-command start --
Session 2 of F268 · round 13 · base `c784f6b3` (branch feature/f268-remedy-do, pushed).

Goal: book round 12's verdict (F268's closure verdict), re-assign R-0892 to F273, rotate the
ledger, then the closure commit — STATUS `[x]`, README, the self-use item consumed, the final
`.agent/` state — and the pull request into `main`. Never merge it.

Read first, completely: AGENTS.md (PR workflow, Rule A4); docs/roadmap/STATUS_closure_protocol.md
Algorithm steps 4 to 6 with the amend0905 rotation and amend0911 ownership paragraphs;
docs/agents/self_drive_protocol.md amend0911-feedback rule A; F266's closure commits `b78eb7e6`,
`2bb64b4b`, `b6d88fdc` and `603f03fa`, the shape to follow.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r13/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md    sha256 223aa2eb4554deb03ca8b07ddfc72cae976b179f1023755fc926ce8a11fdbe8e
  plan.md      sha256 a0e01933ed55ac23be79f1361ef84a3547ef3a9a3ca9764825c4d8dec9b1282d
  pairs.json   sha256 11aaea9655a636ac30dd13ae0a3883dad108edb1917cf2b9be0fe6cca1a08f0a
  pr_body.md   sha256 18bf4e32de5a22ceee93f52c2557bbdeace1b60786494f9c6ae090501e4c3a2c
  block.md     this block (save it as `.agent/authored/f268-r13-block.md`; report its digest)
`pairs.json` maps a commit label to `{path: [[FROM, TO], ...]}`. Apply every pair of a label
with a python script that asserts each FROM occurs exactly once before and each TO exactly once
after (the reviewer measured both at `c784f6b3`; no TO contains its FROM), in list order.

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f268-r13-<name>`;
   `.agent/live_review.md` := (`git show c784f6b3:.agent/live_review.md` bytes with the C1 pair
   for that path applied) + ledger.md; `docs/roadmap/features/T2_F273.md` := its `c784f6b3`
   bytes with the C1 pair for that path applied.
C2 rotation — one commit whose path set is exactly `.agent/live_review.md` and
   `.agent/live_review_archive.md`: `python3 scripts/rotate_live_review.py`; record the old and
   new ledger sizes and the open-findings count before and after, which must be equal.
C3 THE CLOSURE COMMIT — the last commit on the branch (Rule A4), path set exactly
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`, `.agent/plan.md` and
   `.agent/handoff.md`: apply every C3 pair; `.agent/plan.md` := plan.md; rewrite
   `.agent/handoff.md` per docs/agents/handback_template.md — "SESSION 2 of feature F268 ·
   round 13 · rounds so far 13", per-commit tables with `git show --numstat` counts for C1 and
   C2, every gate's real output, the grep proof that the STATUS line and the README paragraph in
   the tree are byte-identical to the payload's TO strings, the rotation sizes, and in `## Next`
   "Phase 1 rule 1 (`.agent/STOP`), then rule 2: merge F268's pull request at the Open PR Gate"
   and "Operator questions open: <the count you read from the file>". It cannot name the PR
   number. Then `git push`.
C4 the pull request — after the push: `gh pr create --base main --head feature/f268-remedy-do
   --title "F268 — remedy do: the one-command start" --body-file <the pr_body.md copy>`. Report
   the PR number and URL in your final message only; no further commit.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. A red gate: stop and report; never edit a payload or a test to pass. No merge, no force-push.
4. Build every edited file from `git show c784f6b3:<path>` bytes.
5. Commit messages "F268 R13 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no other line of `docs/roadmap/STATUS.md`, README.md or `T2_F273.md`.

Done when (G1 and G2 after C2; G3 to G5 on C3's tree before its commit; G6 after C4):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` at C1 equals its `c784f6b3` bytes with the owner pair applied plus
   ledger.md, and that `T2_F273.md` at C1 equals its `c784f6b3` bytes with its pair applied.
G2 the rotation script's own output and the open-findings count before and after, equal.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py` -> 0
   failed (the reviewer's dry run at `c784f6b3` with the C3 pairs applied read `310 passed` for
   `tests/docs/`, and `1 failed` with the README count left at 81).
G4 `packages.orchestration.integrity_gate.run_integrity_checks()` -> passed.
G5 the STATUS line and the README paragraph byte-identical to the payload's TO strings (count 1
   each in the tree).
G6 `git status --porcelain` empty; local tip equals origin; `gh pr view --json
   number,state,baseRefName,headRefName,isDraft` reads OPEN, base `main`, not a draft.
-- end of block --
