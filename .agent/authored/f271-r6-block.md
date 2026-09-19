-- STEP R6 closure round B -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 6 · base `90c03d14` (branch `feature/f271-no-more-legacy`, pushed).

Goal: book round 5's verdict (F271's closure verdict) and one prose-slip line, rotate the ledger,
then the closure commit — STATUS `[x]`, README, the self-use item consumed, the final `.agent/`
state — and the pull request into `main`. Never merge it.

Read first, completely: AGENTS.md (PR workflow, Rule A4); docs/roadmap/STATUS_closure_protocol.md
Algorithm steps 4 to 6 with the amend0905 rotation paragraph; F270's closure commits `be80be80`,
`80c23593` and `b91fb1ec`, the shape to follow.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r6/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md             sha256 1afb1651eecb1a802255084d639b8b5726fa0f87fa6a71ffbb99cc8f3ca744f0
  slips.md              sha256 67848d24c640225e1ad94ef2230a13b1ced78276d18889d26a3a2916dec3c85f
  plan.md               sha256 d33311bf5ff862cc22db95d94dc9b17f38df4304a4ba89cc4647c12159127c89
  status_line.txt       sha256 d4939a7c33c5a109d07c45e310ba3182121c701e4b659e91590f5e6b3ef7f923
  readme_paragraph.txt  sha256 59bebfc6d8a0e744a40d1a69405b232954500ca79c8591b53381ad5e0a94ba12
  pairs.py              sha256 b66663b0e0e8d4890f0c2f07680331430be77eea745efc835e04644f4e4d976e
  pr_body.md            sha256 4b382654e5526c9254543ab870acfec12e26b64c8625a38ad638f045681553ba
  block.md              this block (save it in C1 with the others; report its digest)
`pairs.py <tree>` applies the closure pairs to a tree — the STATUS line, the README counters and
paragraph, SU-022's `consumed_by` — asserting each FROM occurs exactly once before and each TO
exactly once after; the reviewer dry-ran it at `90c03d14` after C1 and C2. Run it on the primary
checkout's root; never hand-edit those files.

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload, the block included, as
   `.agent/authored/f271-r6-<name>`; `.agent/live_review.md` := its `90c03d14` bytes + ledger.md;
   `.agent/prose_slips.md` := its `90c03d14` bytes + slips.md.
C2 rotation — one commit whose path set is exactly `.agent/live_review.md` and
   `.agent/live_review_archive.md`: `python3 scripts/rotate_live_review.py`; record its output (the
   reviewer's dry run on C1's ledger read 3 finding pairs moved, 587543 to 559697 bytes, open
   findings 129 before and 129 after by the script's own count).
C3 THE CLOSURE COMMIT — the last commit on the branch (Rule A4), path set exactly
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json`, `.agent/plan.md` and
   `.agent/handoff.md`: `python3 .remedy-wt/f271-r6/pairs.py .`; `.agent/plan.md` := plan.md;
   rewrite `.agent/handoff.md` per docs/agents/handback_template.md — "SESSION 1 of feature F271 ·
   round 6 · rounds so far 6" plus one sentence of context self-assessment, per-commit tables with
   `git show --numstat` counts for C1 and C2, every gate's real output, the grep proof that the
   STATUS line and the README paragraph in the tree are byte-identical to status_line.txt and
   readme_paragraph.txt, the rotation output, open findings by distinct id measured on the
   committed ledger, and in `## Next` "Phase 1 rule 1 (`.agent/STOP`), then rule 2: merge F271's
   pull request at the Open PR Gate" and "Operator questions open: <the count you read from the
   file>". It cannot name the PR number. Then `git push`.
C4 the pull request — after the push: `gh pr create --base main --head feature/f271-no-more-legacy
   --title "F271 — No more legacy: ownership, reachability, replace-is-delete" --body-file
   .agent/authored/f271-r6-pr_body.md`. Report the PR number and URL in your final message only;
   no further commit.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp` and `sed -i` — copy bytes with python.
3. A red gate: stop and report; never edit a payload or a test to pass. No merge, no force-push.
4. Build every appended file from `git show 90c03d14:<path>` bytes.
5. Commit messages "F271 R6 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Touch no other line of `docs/roadmap/STATUS.md`, README.md or the queue.

Done when (G1 and G2 after C2; G3 to G5 on C3's tree before its commit; G6 after C4):
G1 transport + state: payload digests matched; a python check prints True that
   `.agent/live_review.md` and `.agent/prose_slips.md` at C1 equal their `90c03d14` bytes plus
   ledger.md and slips.md, and that each `.agent/authored/f271-r6-*` copy equals its payload.
G2 the rotation script's own output, its open-findings count before and after equal.
G3 `python3 -m pytest -q -p no:cacheprovider tests/docs/ tests/cli/test_golden_path.py
   tests/cli/test_advertised_commands.py tests/orchestration/test_roadmap_index.py
   tests/orchestration/test_live_review_rotation.py` -> 0 failed (the reviewer's dry run with every
   pair applied read `406 passed`).
G4 `packages.orchestration.integrity_gate.run_integrity_checks()` -> passed.
G5 the STATUS line and the README paragraph byte-identical to the payload files (count 1 each in
   the tree), and `SU-022`'s `consumed_by` reads `F271`.
G6 `git status --porcelain` empty; local tip equals origin; `gh pr view --json
   number,state,baseRefName,headRefName,isDraft` reads OPEN, base `main`, not a draft.
-- end of block --
