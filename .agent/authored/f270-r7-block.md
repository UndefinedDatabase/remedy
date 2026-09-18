-- STEP R7 closure round B -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 7 · base `b1e5e846` (branch feature/f270-history-apply, pushed).

Goal: book round 6's verdict (F270's closure verdict), rotate the ledger, then the closure commit —
STATUS `[x]`, README, the self-use item consumed, the final `.agent/` state — and the pull request
into `main`. Never merge it.

Read first, completely: AGENTS.md (PR workflow, Rule A4); docs/roadmap/STATUS_closure_protocol.md
Algorithm steps 4 to 6 with the amend0905 rotation paragraph; F269's closure commits `7a09c914`,
`2dbc74fe` and `35f209f4`, the shape to follow.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r7/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md             sha256 9476686515e3ea73e67a2b3d80e70bba8b28b21efd39cc01b3aff53a540d5ce7
  plan.md               sha256 995b0590c33e5e3f4aeb182cfc57201dbc2552441f95906b62d3978169a93dbf
  status_line.txt       sha256 d53c159bc198150361b7fb27b186f74cd2c07ba517645ca5011017822bd8c743
  readme_paragraph.txt  sha256 c4ca779b280e5431dde575d3bfc4a4d434a2feb8ff65762d6a7bb3bbb0ef4e69
  pairs.py              sha256 b79b522df40d674461514558a4519bec73bc31002d3208695230c3fc9e2b806e
  pr_body.md            sha256 2319e04c1e9cb9b2e7586f035ad00cbf654a6bc2e54124cbe8761b61e4a15382
  block.md              this block (save it in C1 with the others; report its digest)
`pairs.py <tree>` applies the closure pairs to a tree — the STATUS line, the README counters and
paragraph, SU-021's `consumed_by` — asserting each FROM occurs exactly once before and each TO
exactly once after; the reviewer dry-ran it at `b1e5e846` after C1 and C2. Run it on the primary
checkout's root; never hand-edit those files.

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload, the block included, as
   `.agent/authored/f270-r7-<name>`; `.agent/live_review.md` := its `b1e5e846` bytes + ledger.md.
C2 rotation — one commit whose path set is exactly `.agent/live_review.md` and
   `.agent/live_review_archive.md`: `python3 scripts/rotate_live_review.py`; record its output (the
   reviewer's dry run on C1's ledger read 13 gate records and 3 finding pairs moved, 128 open before
   and after).
C3 THE CLOSURE COMMIT — the last commit on the branch (Rule A4), path set exactly
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`, `.agent/plan.md` and
   `.agent/handoff.md`: `python3 .remedy-wt/f270-r7/pairs.py .`; `.agent/plan.md` := plan.md;
   rewrite `.agent/handoff.md` per docs/agents/handback_template.md — "SESSION 1 of feature F270 ·
   round 7 · rounds so far 7" plus one sentence of context self-assessment, per-commit tables with
   `git show --numstat` counts for C1 and C2, every gate's real output, the grep proof that the
   STATUS line and the README paragraph in the tree are byte-identical to status_line.txt and
   readme_paragraph.txt, the rotation output, and in `## Next` "Phase 1 rule 1 (`.agent/STOP`),
   then rule 2: merge F270's pull request at the Open PR Gate" and "Operator questions open: <the
   count you read from the file>". It cannot name the PR number. Then `git push`.
C4 the pull request — after the push: `gh pr create --base main --head feature/f270-history-apply
   --title "F270 — History apply: one commit per task, merge on demand" --body-file
   .agent/authored/f270-r7-pr_body.md`. Report the PR number and URL in your final message only;
   no further commit.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp` and `sed -i` — copy bytes with python.
3. A red gate: stop and report; never edit a payload or a test to pass. No merge, no force-push.
4. Build every appended file from `git show b1e5e846:<path>` bytes.
5. Commit messages "F270 R7 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no other line of `docs/roadmap/STATUS.md`, README.md or the queue.

Done when (G1 and G2 after C2; G3 to G5 on C3's tree before its commit; G6 after C4):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` at C1 equals its `b1e5e846` bytes plus ledger.md, and that each
   `.agent/authored/f270-r7-*` copy equals its payload.
G2 the rotation script's own output, its open-findings count before and after equal.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
   tests/cli/test_advertised_commands.py tests/orchestration/test_roadmap_index.py
   tests/orchestration/test_live_review_rotation.py` -> 0 failed (the reviewer's dry run with every
   pair applied read `406 passed`).
G4 `packages.orchestration.integrity_gate.run_integrity_checks()` -> passed.
G5 the STATUS line and the README paragraph byte-identical to the payload files (count 1 each in
   the tree), and `SU-021`'s `consumed_by` reads `F270`.
G6 `git status --porcelain` empty; local tip equals origin; `gh pr view --json
   number,state,baseRefName,headRefName,isDraft` reads OPEN, base `main`, not a draft.
-- end of block --
