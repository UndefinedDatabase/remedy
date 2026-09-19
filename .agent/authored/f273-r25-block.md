-- STEP R25 closure round B: ownership, rotation, F282, the closure commit, the PR -- F273 Findings paydown v1 --
Session 4 of F273 · round 25 · base `94e6fa87` (the round 24 handoff, branch
`feature/f273-findings-paydown-v1`, pushed).

Goal: book round 24's verdict, R-1000's registration and the ownership paragraph; rotate the
ledger; register F282, the next findings-paydown feature (amend0911-feedback rule B); then the
closure commit (STATUS `[x]`, README, the self-use item consumed, the handoff) and the pull request
into `main`. Never merge it.

Read first, completely: AGENTS.md (Commit Discipline, PR workflow, Rule A4);
docs/roadmap/STATUS_closure_protocol.md Algorithm steps 4 to 6 with the amend0905 rotation and the
amend0911 paragraphs; F271's closure commits `c9401ad0` and the one after it, the shape to follow.

PAYLOADS: reviewer-authored, gitignored scratch in `.remedy-wt/f273-r25/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md             sha256 2a06166b3687ec59e2995e88204fef183fe27daf5afed9b5e1f13d20dad8d62b
  plan.md               sha256 eb595b40c3d20282d6b3c2a73abb2872670ac563e607a726edd5a6088dd6e745
  next.md               sha256 4a3475825e51594ce85d222bab14609df82accc1d40c884924b95e4d13f1522c
  T2_F282.md            sha256 d9e85eb0e4910ec6e0aa4b3cf5b10023dbf84e6aa746fec04027343cf8d010de
  status_line.txt       sha256 45fc4fcb9b5099a81232999a1eecfa7b9ca0977da162d7f4092e96d66f047cb5
  readme_paragraph.txt  sha256 d8579af9266aad134d4f263bb9a7b940d650f1047acad8919b33d674b2ed73e3
  pairs.py              sha256 7e85a83886b132074224cbf65b2c385831198cdd84176f3bd67aac5437ce4d1d
  pr_body.md            sha256 3c5bdf75d281c3c2fbfbc2ff327a40ac11c1d10a14b9397074596e9198983a34
  block.md              this block (save it; report its sha256 and line count)
`python3 .remedy-wt/f273-r25/pairs.py reg .` writes F282's feature file and applies the
registration pairs; `... pairs.py close .` applies the closure pairs. Each asserts every FROM once
before and every TO once after. Run both from the repository root; never hand-edit those files.

Bundle (commit order):
C1 bookkeeping, one commit: byte copies of every payload above but next.md, the block included, as
   `.agent/authored/f273-r25-<name>`; `.agent/live_review.md` := its `94e6fa87` bytes + ledger.md;
   `.agent/plan.md` := plan.md. Before this commit, compare the saved block copy's line count and
   sha256 with the block text you were given, and report both.
C2 rotation, one commit whose path set is exactly `.agent/live_review.md` and
   `.agent/live_review_archive.md`: `python3 scripts/rotate_live_review.py`. The reviewer's dry run
   on C1's ledger read 6 gate records and 134 finding pairs moved, 718386 to 361092 bytes, 14 open
   findings before and after, and 612 inserted lines. That is over 500: C2 is F273's ONE declared
   oversize commit (AGENTS.md, Commit Discipline), and the handoff declares it with this reason:
   "the rotation script moves the records byte-verbatim in one pass and verifies each moved
   record's sha256 before and after; a split would leave a record in neither file or in both".
C3 F282's registration, one commit whose path set is exactly `docs/roadmap/features/T2_F282.md`,
   `docs/roadmap/STATUS.md`, `tests/docs/test_docs_consistency.py` and `README.md`:
   `python3 .remedy-wt/f273-r25/pairs.py reg .`.
C4 THE CLOSURE COMMIT, the last commit on the branch (Rule A4), path set exactly
   `docs/roadmap/STATUS.md`, `README.md`, `scripts/self_use_queue.json` and `.agent/handoff.md`:
   `python3 .remedy-wt/f273-r25/pairs.py close .`; rewrite `.agent/handoff.md` per
   docs/agents/handback_template.md: "SESSION 4 of feature F273 · round 25 · rounds so far 25" plus
   one sentence of context self-assessment; per-commit tables with `git show --numstat` counts for
   C1 to C3; the oversize declaration of C2; every gate's real output; the rotation's output; the
   grep proof that the STATUS line and the README paragraph in the tree are byte-identical to
   status_line.txt and readme_paragraph.txt; open findings by distinct id on the committed ledger;
   under External actions the `remedy/job-*` branch count and that the branches
   `remedy/job-81ec65896729405c` and `remedy/job-468c8e62a2cc4fac` and the worktree
   `.remedy-wt/job-468c8e62a2cc4fac` still exist, which nobody may delete without the operator; a
   `## Next` section whose body is next.md byte for byte; and the line "Operator questions open:
   <the count you read from the file>". It cannot name the PR number. Then `git push`.
C5 the pull request, after the push: `gh pr create --base main --head
   feature/f273-findings-paydown-v1 --title "F273 — Findings paydown v1" --body-file
   .agent/authored/f273-r25-pr_body.md`. No further commit.

Constraints:
1. Change set: the paths the Bundle names. Every commit but C2 < 500 inserted lines.
2. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR` (including `$?`), heredocs and `cd`
   before git. Use `git -C <path>` and small python scripts under `.remedy-wt/f273-r25/`, named
   `wk_*.py`, with an explicit `cwd=`. Never use `git stash`.
3. A red gate: stop, commit nothing half-done, report. Never edit a payload or a test to pass.
4. Build every appended file from `git show 94e6fa87:<path>` bytes.
5. Commit messages read "F273 R25 C<n>: <summary>", then a blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit. No merge,
   no force-push.
6. Touch no other line of STATUS, README, the queue or the pin file. No `.claude/**`, no production
   code, no `remedy` CLI, no self-use runner, no zip. Create, delete or remove no branch or worktree.
   Do not run the full suite (amend0917-throughput (1)).

Done when (report literal output and the real exit code):
G1 after C1: payload digests matched; a python check prints True that `.agent/live_review.md`
   equals its `94e6fa87` bytes + ledger.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f273-r25-*` copy equals its payload.
G2 C2: the rotation script's own output, its open-findings count before and after equal, and
   `git show --numstat` of C2.
G3 after C3: `git rev-parse <C3>:docs` prints 375d7c6cbc95250dec300de0cf8f6746190f3de4 and
   `git rev-parse <C3>:tests` prints b84dc9ab4f1cb1e90d61b686c8b4ef2c8c64c71b (the reviewer's
   dry-run objects), and `python3 -m pytest -q -p no:cacheprovider tests/docs/
   tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py` -> 0 failed.
G4 on C4's tree after `pairs.py close` and before the C4 commit: `python3 -m pytest -q -p
   no:cacheprovider tests/docs/ tests/orchestration/test_roadmap_index.py
   tests/cli/test_golden_path.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_generator.py
   tests/cli/test_advertised_commands.py` -> 0 failed (the reviewer's dry run read `459 passed`);
   `packages.orchestration.integrity_gate.run_integrity_checks()` -> passed; the STATUS line and
   the README paragraph each occur once in the tree, byte-identical to their payloads; SU-023's
   `consumed_by` reads `F273`.
G5 after C5: `git status --porcelain` empty; the local tip equals origin; `gh pr view --json
   number,state,baseRefName,headRefName,isDraft,url` reads OPEN, base `main`, not a draft. Report
   this in your final message only.
-- end of block --
