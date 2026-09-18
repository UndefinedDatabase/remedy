-- STEP R1 T001 -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 1 · base `a4f79a94` (main, the merge of pull request 258).

Goal: claim F271, land T001 — `feature` and `reach` on every `GroupDef`, refused by a catalog
test with red proof — and delete `builder_eval.py` under DECISION amend0911-feedback D6.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F271.md; the payload `decisions.md`
(DECISION F271 D1 — this round's spec; where this block is terser, it rules). A REFERENCE, not a
slice: `.remedy-wt/f271-r1/prototype2.diff` (sha256
e6270600ca4a4c4281cd3e4e5744bf7cef04bd802df2cef600b51ce938a164ff) is a research helper's
prototype of C2 and C3, built at `a4f79a94`. Read it; you may apply its hunks after reading them,
but you own every line you commit and D1 rules where the two differ.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r1/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 d0988fdc61f06932ad1f10af7fd0df78bc87f1666c9dbe1a4bc035bc58232345
  context.md           sha256 f30320b9d39e8c85cb04fa361c9fb3026a30c22a8e990d0289cf361b0820ddc6
  live_review_head.md  sha256 d43d01bbe86d913b2bb1e8a4856d6a00bd315fe4e409e5a6c43445a1fe361368
  ledger.md            sha256 9c5608a42d8dbe093fa4264fd771234b6c925f44f47ddd5bacbc3bfe11006bab
  decisions.md         sha256 74560aa1a0ebb49d3ae22fd503fd7761057ea049d3a2178cec190b5f1806c15b
  status_from.txt      sha256 cd428377d7667c897eee89f34954df8b694e961e9e1e667e4e9189ac37b7ba8f
  status_to.txt        sha256 11eb85f4255f6e6354e67c96a869667f1f1f27c9b5234a63d8c0e643dc2399cd
  brain_from.txt       sha256 e55ef39cffe87362c11acaf0e82a70080437b6667f2040d2be7ad7d4052ccf8d
  brain_to.txt         sha256 d2dd82153f50cf40351531bd703c2ae314f3052f4c883b05474aedf99b4db7c9
  block.md             this block (save it; report its digest)

Bundle (commit order):
C1 claim — branch `feature/f271-no-more-legacy` from `main` at `a4f79a94` (the reviewer already
   ran the Open PR Gate: it merged pull request 258; zero pull requests are open). One commit
   holding exactly: byte copies of every payload above as `.agent/authored/f271-r1-<name>`;
   `.agent/plan.md` := plan.md; `.agent/context.md` := context.md; `.agent/live_review.md` :=
   live_review_head.md bytes + the old file's bytes from the line `## Findings` (inclusive) to the
   end + ledger.md bytes (it books F270 round 8's verdict and `Done: R-0979`); `.agent/decisions.md`
   := old bytes + decisions.md bytes; `docs/roadmap/STATUS.md`: the line equal to status_from.txt
   replaced by status_to.txt (reviewer's containment test: `TO contains FROM: False`, a REWRITE —
   FROM 1x before, 0x after, TO 1x after).
C2 T001 — per D1 (1) to (3): `Reach` and the two defaulted `GroupDef` fields in
   `apps/cli/command_catalog.py`, every entry of `GROUPS` annotated by keyword with D1 (3)'s
   owner and reach, and in `tests/test_command_catalog.py` a `TestGroupOwnership` class: the
   shipped groups have no violation; planted groups (no feature, no reach, a reach outside
   `Reach`, a well-formed but unregistered feature such as `F999`) yield exactly their refusals.
   The STATUS lookup reads `docs/roadmap/STATUS.md` from the repository root derived from the
   test file's own path.
C3 deletion — per D1 (4): `git rm` of `packages/orchestration/builder_eval.py`,
   `tests/orchestration/test_builder_eval.py` and `scripts/remedy_builder_eval.sh`; the
   `"test_builder_eval.py",` line removed from `REAL_OLLAMA_FILES` in `tests/conftest.py`;
   `docs/system/project-brain.md`: the bytes of brain_from.txt replaced by brain_to.txt
   (reviewer's containment test: `TO contains FROM: False`, a REWRITE — FROM 1x before, 0x after,
   TO 1x after).
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F271 · round 1 · rounds so far 1" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id, measured on the committed ledger; `## Next` naming
   Phase 1 rule 1 then the review of round 1, and "Operator questions open: <the count you read
   from the file>". Then `git push -u origin feature/f271-no-more-legacy`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F271.md): the reachability allowlist, the dead-model check, the catalog's
   command set; no command is added, removed or renamed.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass, other than the D6 deletion itself. A red
   gate or an ambiguity D1 does not settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` and `docs/` file from `git show a4f79a94:<path>` bytes.
6. Commit messages "F271 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` and `.agent/context.md` equal their payloads, that `.agent/live_review.md`
   equals head + the `a4f79a94` bytes from `## Findings` + ledger.md, that `.agent/decisions.md`
   equals its `a4f79a94` bytes + decisions.md, that STATUS and project-brain.md equal their
   `a4f79a94` bytes with their pair applied, and that each `.agent/authored/f271-r1-*` copy
   equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/test_command_catalog.py tests/cli/test_cli_ux.py
   tests/test_help_renderer.py tests/test_grouped_cli.py tests/cli/test_command_catalog.py
   tests/cli/test_advertised_commands.py tests/orchestration/test_import_reachability.py
   tests/test_imports.py tests/orchestration/test_roadmap_index.py
   tests/orchestration/test_project_summary.py tests/cli/test_smoke_scripts.py
   tests/orchestration/test_dead_command_check.py tests/cli/test_worker_facade_cmd.py
   tests/cli/test_golden_path.py tests/docs/` → summary line, 0 failed (serial, no `-n`).
G3 `python3 -m ruff check apps/cli/command_catalog.py tests/test_command_catalog.py
   tests/conftest.py` → "All checks passed!".
G4 `git grep -n -e builder_eval -e remedy_builder_eval -- . ':!.agent' ':!docs/roadmap'` prints
   nothing (exit 1), and the three deleted paths are absent from `git ls-tree -r --name-only` of C3.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest -q -p no:cacheprovider tests/test_command_catalog.py -k
   TestGroupOwnership`, `__pycache__` purged before each run, the imported `command_catalog`
   module path printed first to prove it resolves inside the worktree; the UNMUTATED control
   first (exit 0); each mutation applied to the single `"ci":` entry line of `GROUPS` in
   `apps/cli/command_catalog.py` (count it: 1) and reverted before the next: (a) its `feature=`
   argument removed; (b) its reach set to `"dev-path"`; (c) its feature set to `"F999"`. Each
   must fail the shipped-groups test; report exit codes and failing ids, and report a mutation
   that stays green as green. Remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
