-- STEP R12 closure round B -- F269 Contract & contract templates --
Session 2 of F269 · round 12 · base `d5b7c9c2` (branch feature/f269-contract, pushed).

Goal: book round 11's verdict (F269's closure verdict) and register R-0972 for F273, rotate the
ledger, then the closure commit — STATUS `[x]`, README, the self-use item consumed, the final
`.agent/` state — and the pull request into `main`. Never merge it.

Read first, completely: AGENTS.md (PR workflow, Rule A4); docs/roadmap/STATUS_closure_protocol.md
Algorithm steps 4 to 6 with the amend0905 rotation and amend0911 ownership paragraphs;
docs/agents/self_drive_protocol.md amend0911-feedback rule A; F268's closure commits `b4aec4f5`,
`ceb91ba9` and `0ecf18ac`, the shape to follow.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r12/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md             sha256 9447ac36229deda4954aae534d9e06903ded8e0069867ea7faac64588153d845
  slips.md              sha256 e861c4acaaee7816229cf792d0cca9b52187bfdb8bf7ac66a67b872b997f520e
  plan.md               sha256 17d45cd63e4417026791283901d129a3ccc1712a0e7c2045eb0f5aba22852842
  f273_acceptance.txt   sha256 6cace0409493b0c5ab63db62315c22786d1834990482622f85092b05506f3756
  status_line.txt       sha256 d296e23cb5b8c1c60555ebe3f266be9c3973b7200f8dbc233156c55baeec505a
  readme_paragraph.txt  sha256 a26022f8a7f5cea22f0aee07fe10d2fda344635f480aeb9d80c5f0e8d9b63313
  pairs.py              sha256 b16936fa19564ea3f8c4a0494354d96ff8904d7030b3a3465bdfe946b547a70d
  pr_body.md            sha256 4ba69a4030ae691d7ca56e2cd310f4ed091de9edf66f13f9882714f4ed3b92a9
  block.md              this block (save it as `.agent/authored/f269-r12-block.md`; report its digest)
`pairs.py <tree> <label>` applies the label's FROM/TO pairs to a tree, asserting each FROM
occurs exactly once before and each TO exactly once after; the reviewer dry-ran both labels at
`d5b7c9c2`. Run it on the primary checkout's root; never hand-edit those files.

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload but pairs.py as
   `.agent/authored/f269-r12-<name>`; `.agent/live_review.md` := its `d5b7c9c2` bytes + ledger.md;
   `.agent/prose_slips.md` := its `d5b7c9c2` bytes + slips.md;
   `python3 .remedy-wt/f269-r12/pairs.py . C1` (the R-0972 Acceptance line in
   `docs/roadmap/features/T2_F273.md`, amend0911-feedback rule A).
C2 rotation — one commit whose path set is exactly `.agent/live_review.md` and
   `.agent/live_review_archive.md`: `python3 scripts/rotate_live_review.py`; record the old and
   new ledger sizes and the open-findings count before and after, which must be equal (the
   reviewer's dry run on C1's ledger read 13 gate records and 1 pair moved, 125 before and after).
C3 THE CLOSURE COMMIT — the last commit on the branch (Rule A4), path set exactly
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`, `.agent/plan.md` and
   `.agent/handoff.md`: `python3 .remedy-wt/f269-r12/pairs.py . C3`; `.agent/plan.md` := plan.md;
   rewrite `.agent/handoff.md` per docs/agents/handback_template.md — "SESSION 2 of feature F269 ·
   round 12 · rounds so far 12" plus one sentence of context self-assessment, per-commit tables
   with `git show --numstat` counts for C1 and C2, every gate's real output, the grep proof that
   the STATUS line and the README paragraph in the tree are byte-identical to status_line.txt
   and readme_paragraph.txt, the rotation sizes, and in `## Next` "Phase 1 rule 1
   (`.agent/STOP`), then rule 2: merge F269's pull request at the Open PR Gate" and "Operator
   questions open: <the count you read from the file>". It cannot name the PR number. Then
   `git push`.
C4 the pull request — after the push: `gh pr create --base main --head feature/f269-contract
   --title "F269 — Contract & contract templates" --body-file .agent/authored/f269-r12-pr_body.md`.
   Report the PR number and URL in your final message only; no further commit.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp` and `sed -i` — copy bytes with python.
3. A red gate: stop and report; never edit a payload or a test to pass. No merge, no force-push.
4. Build every appended file from `git show d5b7c9c2:<path>` bytes.
5. Commit messages "F269 R12 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no other line of `docs/roadmap/STATUS.md`, README.md, `T2_F273.md` or the queue.

Done when (G1 and G2 after C2; G3 to G5 on C3's tree before its commit; G6 after C4):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` and `.agent/prose_slips.md` at C1 equal their `d5b7c9c2` bytes plus
   their payload, and that the authored copies equal their payloads.
G2 the rotation script's own output and the open-findings count before and after, equal.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py` -> 0
   failed (the reviewer's dry run with both labels applied read `352 passed`).
G4 `packages.orchestration.integrity_gate.run_integrity_checks()` -> passed.
G5 the STATUS line and the README paragraph byte-identical to the payload files (count 1 each in
   the tree), and `SU-020`'s `consumed_by` reads `F269`.
G6 `git status --porcelain` empty; local tip equals origin; `gh pr view --json
   number,state,baseRefName,headRefName,isDraft` reads OPEN, base `main`, not a draft.
-- end of block --
