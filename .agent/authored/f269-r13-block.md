-- STEP R13 CI repair -- F269 Contract & contract templates --
Session 3 of F269 · round 13 · base `35f209f4` (branch feature/f269-contract, pushed; pull request
257 into `main`, open).

Goal: repair pull request 257's hosted CI under AGENTS.md's Open PR Gate exception
(amend0820-gate-autonomy): run `35372747359` on `35f209f4` failed one node,
`tests/cli/test_advertised_commands.py::test_every_group_only_advertisement_reaches_a_command`,
because `README.md` line 145 advertises `remedy do --contract`, a form that reaches no command.

Read first, completely: AGENTS.md (Commit Gate, Open PR Gate); the payload `ledger.md` (it
registers R-0973 — the finding text is this round's spec).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r13/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md        sha256 6e3c6d4aceaad3b258b7c2ed8a4bead56d9526e786317775a44c27382b5b0812
  slips.md         sha256 523fb4ffd55cdbec81c871eb2fe35f91047d461c9a92e40eaff6017416c530f4
  plan.md          sha256 fa2c3cc643786d4af6a2f5bcf5f7ff6c573b2c721e9df6bf05456dee250578b3
  readme_from.txt  sha256 5322be495bf459de3a9c5750553fdff6d8cbd3065b2e1c5d4774bbce0b257ddc
  readme_to.txt    sha256 005316485f834e126f306adf5743c656c2931b4a15855b61d8b02d5ddee412ee
  block.md         this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of every payload above as
   `.agent/authored/f269-r13-<name>`; `.agent/live_review.md` := its `35f209f4` bytes + ledger.md
   (it books round 12's verdict and registers R-0973); `.agent/prose_slips.md` := its `35f209f4`
   bytes + slips.md; `.agent/plan.md` := plan.md.
C2 the repair — in `README.md` the bytes of readme_from.txt (exactly 1x at `35f209f4`) replaced by
   the bytes of readme_to.txt. The reviewer's containment test on the pair printed
   `TO contains FROM: False`, so a REWRITE: FROM 1x before and 0x after, TO 1x after. Nothing else
   in the file changes; the guard test is not edited.
C3 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 3 of feature F269 · round 13 · rounds so far 13" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 and C2; every gate's
   real output; open findings by distinct id; `## Next` naming Phase 1 rule 1, then the review of
   round 13 and the Open PR Gate on pull request 257 after its hosted CI, and "Operator questions
   open: <the count you read from the file>". Then `git push` (never force).

Constraints:
1. Change set: exactly the paths the Bundle names. Every commit < 500 inserted lines.
2. Build every edited file from `git show 35f209f4:<path>` bytes. The shell denies `VAR=x cmd` and
   `cp`; copy and compare bytes with python.
3. Never weaken an assertion, edit the guard or delete a test to pass. A red gate or an ambiguity
   → stop, commit nothing half-done, report.
4. Do not merge, comment on or edit pull request 257; the reviewer does that.
5. Commit messages "F269 R13 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G3 at C2, before C3; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` and `.agent/prose_slips.md` equal
   their `35f209f4` bytes + ledger.md and + slips.md, and that each `.agent/authored/f269-r13-*`
   copy equals its payload.
G2 the pair: `README.md` holds readme_from.txt 0x and readme_to.txt 1x; `git show --numstat` of C2
   lists `README.md` alone.
G3 `python3 -m pytest -q -p no:cacheprovider tests/cli/test_advertised_commands.py tests/docs/
   tests/cli/test_golden_path.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` → summary
   line, 0 failed (serial, no `-n`).
G4 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput); the hosted CI re-runs it on the push.
-- end of block --
