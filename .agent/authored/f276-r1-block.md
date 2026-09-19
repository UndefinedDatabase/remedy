-- STEP R1 T001 -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 1 · base `43d14817` (main, the merge of pull request 260, F273's closure).

Goal: claim F276, book F273 round 25's verdict with the colour its pull request asked hosted CI for,
register and repair R-1001, and build T001 exactly as the reviewer's dry run built it.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISIONs F276 D1 and D2 — this round's spec; where this block is terser, they rule).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r1/`. Verify each sha256 before
use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 10d14dab018660fe34a18d6673e7e81394a11c79edd938dbd0a8c8de5091b121
  context.md           sha256 c3d383e45a3b5785696a11c3f61d82dcd7625f800e1311070b683ab15024ac76
  live_review_head.md  sha256 0f15e5fe6079d666f4aa3f862f34412f967abb0b2923204b80194a78cfad04d0
  ledger.md            sha256 d2540200532dabdc3a57cdd1e84b5eee3cb1740298a83f0536059fc98e01b58c
  decisions.md         sha256 86480e798bc35c16564c7bcd3bc180f7fdfafa0b73d72ebef930546ea962d0f7
  status_from.txt      sha256 2d1d34c769575f4ef17c1586fe10ae52f84278dc0268a87568a6df8b21fce0f0
  status_to.txt        sha256 1f9b47ef799e660fe82255feb20fc9680f05b15b322942386f962d505435d627
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `43d14817`, applied there,
tested there and red-proved there. Apply it in three disjoint slices with the `--include` lists
below; do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r1/f276-r1.diff` sha256 35a318161ab8c2de5eb01557976128a32c40e9c20abf1fa3f4bbf82dd9f0ccca

Bundle (commit order):
C1 claim — branch `feature/f276-data-root-hygiene` from `main` at `43d14817` (the reviewer already
   ran the Open PR Gate: it merged pull request 260; zero pull requests are open). One commit holding
   exactly: byte copies of every payload above as `.agent/authored/f276-r1-<name>`; `.agent/plan.md`
   := plan.md; `.agent/context.md` := context.md; `.agent/live_review.md` := live_review_head.md
   bytes + the old file's bytes from the line `## Findings` (inclusive) to the end + ledger.md bytes
   (it books F273 round 25's verdict, the hosted-CI reading and R-1001); `.agent/decisions.md` := old
   bytes + decisions.md bytes; `docs/roadmap/STATUS.md`: the line equal to status_from.txt replaced
   by status_to.txt (reviewer's containment test, run mechanically: `TO contains FROM: False`, so a
   REWRITE — FROM 1x before and 0x after, TO 0x before and 1x after).
C2 R-1001 — `git apply --include=tests/cli/test_study_cmd.py .remedy-wt/f276-r1/f276-r1.diff`.
C3 the registry — `git apply --include=packages/orchestration/data_paths.py
   --include=tests/test_data_root_classes.py .remedy-wt/f276-r1/f276-r1.diff`.
C4 footprint, the `data` group and the doc — `git apply` of the SAME diff with
   `--include=packages/orchestration/data_footprint.py --include=apps/cli/command_catalog.py
   --include=apps/cli/commands/__init__.py --include=apps/cli/commands/data_cmd.py
   --include=tests/cli/test_data_cmd.py --include=tests/cli/test_cli_ux.py
   --include=tests/orchestration/test_data_footprint.py
   --include=tests/orchestration/import_reachability_allowlist.txt
   --include=docs/system/architecture.md`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 1 · rounds so far 1" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; a line
   `Landed: R-1001` naming its commit (in the handoff only — never a `Done:` line anywhere); `## Next`
   naming Phase 1 rule 1 then the review of round 1 then T002, and "Operator questions open: <the
   count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push -u origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r1/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D1 and D2 do not settle ->
   stop, commit nothing half-done, report.
4. Build every edited `.agent/` and `docs/` file from `git show 43d14817:<path>` bytes.
5. Commit messages "F276 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root.
7. The production change is DESCRIBED by D1 and CARRIED by the diff: apply it, do not re-derive it.

Done when (G1 to G5 at C4, before C5; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that `.agent/plan.md`
   and `.agent/context.md` equal their payloads, that `.agent/live_review.md` equals head + the
   `43d14817` bytes from `## Findings` + ledger.md, that `.agent/decisions.md` equals its `43d14817`
   bytes + decisions.md, that `docs/roadmap/STATUS.md` equals its `43d14817` bytes with the pair
   applied, and that each `.agent/authored/f276-r1-*` copy equals its payload. Report the saved
   block's line count and sha256 beside the ones this block's own bytes give.
G2 code transport: at C4, `git rev-parse <C4>:packages <C4>:apps <C4>:tests` prints exactly
   0545a9d3450fa2fdb41ac026c192d1e3ac4f7cfa, c57d66e877e5e4a370a9234cfd5fb8a2c6290e61 and
   3ddec410900ee2f3cb14ddb6d7cb2c91b07089bc, and `git rev-parse <C4>:docs/system/architecture.md`
   prints d39a7663e2ed5833715d74cad907e26d69bed610 — the objects of the reviewer's dry run. Also
   `git diff --name-only <C1> <C4>` names exactly the paths C2, C3 and C4 name, and no other; report
   that list and its length.
G3 `python3 -m pytest -q -p no:cacheprovider tests/test_data_root_classes.py
   tests/orchestration/test_data_footprint.py tests/cli/test_data_cmd.py tests/cli/test_study_cmd.py
   tests/test_data_paths.py tests/cli/test_cli_ux.py tests/test_command_catalog.py
   tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_advertised_commands.py
   tests/cli/test_golden_path.py tests/docs tests/orchestration/test_roadmap_index.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/orchestration/test_dead_command_check.py tests/ui_server/test_handler_table_walk.py` in the
   primary checkout, serial (no `-n`) -> summary line, 0 failed, exit 0.
G4 `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/__init__.py
   apps/cli/commands/data_cmd.py packages/orchestration/data_paths.py
   packages/orchestration/data_footprint.py tests/cli/test_cli_ux.py tests/cli/test_data_cmd.py
   tests/cli/test_study_cmd.py tests/orchestration/test_data_footprint.py
   tests/test_data_root_classes.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.data_paths` and `packages.orchestration.data_footprint` paths
   printed first to prove they resolve inside the worktree. The UNMUTATED control first over the four
   files named below (expect exit 0). Then, each reverted byte-identically before the next, the
   mutated bytes counted in the named file first (each count must be 1): (a) a helper
   `def foo_dir(root: Path | None = None) -> Path:` returning `(root if root is not None else
   resolve_data_root()) / "foo"` appended to `packages/orchestration/data_paths.py` ->
   `tests/test_data_root_classes.py` must fail, naming `foo` and its site; (b) in
   `packages/orchestration/data_footprint.py` the line
   `                is_dir = entry.is_dir(follow_symlinks=False)` replaced by
   `                is_dir = True` -> `tests/orchestration/test_data_footprint.py` must fail; (c) the
   single `    "data": GroupDef("data", "Data", ...)` line deleted from `apps/cli/command_catalog.py`
   -> `tests/cli/test_data_cmd.py` and `tests/cli/test_cli_ux.py` must fail. Report each exit code
   and the failing node ids, and a mutation that stays green as green. Restore all three files, show
   that each is byte-identical to before, remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput rule 1).
-- end of block --
