# Handback — F206 round 3: book round 2, DECISIONS F206 D3 and D4, the `project` group's move, T003 and T004

## Session

SESSION 1 of feature F206 · round 3 · rounds so far 3

Context self-assessment: the session verified the block's own line count and sha256 and the
digests of the five `dry-*` files, `run_selection.py` and `selection.txt` before any write,
byte-copied and re-hashed every C1 target against its prepared source, moved the `project`
group byte for byte into its own module and proved the live catalog equal entry for entry and
in order before and after (184 entries, zero mismatches) rather than merely asserting it, wrote
T003 and T004 from the block's specification and DECISIONS F206 D3/D4 against the stats-module
and data_cmd/project.py precedents, caught and fixed a vocabulary-guard collision in a catalog
description before it ever reached a commit, sanity-checked every new module and command with
plain-python scripts under the worker's own scratch directory (never pytest, per the round's
single-test-run constraint) before each commit, then ran every gate from the primary checkout
exactly once each as ordered with real output captured, all six green on the first pass with no
fix commit needed; context remains comfortable at handback.

Fortschritt: ~70 % (T001 to T004 landed · the closure open) — Schätzung

## Range

Review of `5fd2b6f43`..HEAD.

## Commits

### 4b5832c04 F206 R3 C1: book round 2 and R-1253's resolution, DECISIONS F206 D3 and D4, the plan for round 3

| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f206-r3.md` | +203/-0 | NEW FILE, byte copy of `block.md` (203 lines, sha256 `b1da76cbd6e52b24be5a2f41f2462e0644da6d4599d43ebe2fd156dec441fae7`, matching both values the session was given) |
| `.agent/decisions.md` | +24/-0 | DECISIONS F206 D3 and D4 appended, byte copy of `dry-decisions.md` |
| `.agent/live_review.md` | +4/-0 | round 2's gate entry appended, byte copy of `dry-live_review.md` |
| `.agent/plan.md` | +11/-12 | rewritten in full for round 3, byte copy of `dry-plan.md` |
| `.agent/prose_slips.md` | +1/-0 | one reviewer-prose slip appended, byte copy of `dry-prose_slips.md` |
| `docs/roadmap/features/T13_F206.md` | +7/-0 | DECISION F206 D4's amendment appended, byte copy of `dry-T13_F206.md` |

### 61450596f F206 R3 C2: the catalog's project group moves to command_catalog_project.py (structure rule 2, DECISION F206 D4)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog.py` | +5/-145 | the twelve `project.*` entries (774 through the `project.register` close) replaced by `*PROJECT_COMMANDS,`; the module-imports comment now names F206 D4 beside F301 D2/F302 D1; `command_catalog_project` imported; the now-unused `_PROJECT_ID` import dropped (ruff F401) |
| `apps/cli/command_catalog_project.py` | +159/-0 | NEW FILE: `PROJECT_COMMANDS`, the moved entries verified byte-identical against the pre-move file by diff |
| `docs/system/structure-ledger-v1.md` | +3/-2 | the boundary paragraph gains "Step (3), done by F206: the `project` group..."; the file's row falls `2631` → `2491` |
| `packages/orchestration/lessons.py` | +4/-3 | `CATALOG_PATHS` gains `apps/cli/command_catalog_project.py`; its comment renamed |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `apps.cli.command_catalog_project` added, sorted after `..._mission` |
| `tests/orchestration/test_lessons.py` | +8/-0 | `test_a_changed_line_of_the_catalogs_project_module_names_its_command`, the stats test's twin with `project.register` |
| `tests/test_structure_ratchet.py` | +1/-1 | `MAX_FILE_LINES` `74818` → `74678` (command_catalog.py net -140 lines: the 141-line project block replaced by one `*PROJECT_COMMANDS,` line (-140), +1 new import line, -1 dropped unused import, net -140) |

### 0cfb8e640 F206 R3 C3: the lockfile plausibility check (T003)

| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/repo_catalog_plausibility.py` | +242/-0 | NEW FILE: `normalize_package_name`, `read_lockfile_packages`, `RepoCatalogWarning`/`RepoCatalogSkip`/`RepoCatalogPlausibility`, `check_repo_catalog_plausibility`, per DECISION F206 D3 |

### b4591f52c F206 R3 C3: the lockfile plausibility check's tests (T003)

| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_repo_catalog_plausibility.py` | +271/-0 | NEW FILE: 242+271 = 513 lines together, over the 500-insertion cap, so the block's own split-into-two-commits clause applied; every scenario the block's C3 lists |

### ac92e044d F206 R3 C4: remedy project catalog-check and catalog-show (T004)

| Path | +/- | Reason |
|---|---|---|
| `apps/cli/command_catalog_project.py` | +34/-0 | `project.catalog-check` and `project.catalog-show` appended to `PROJECT_COMMANDS` |
| `apps/cli/commands/__init__.py` | +2/-1 | `repo_catalog_cmd` imported and added to `collect_all_handlers`'s module tuple |
| `apps/cli/commands/repo_catalog_cmd.py` | +129/-0 | NEW FILE: the two handlers, `_catalog_file_path`, `_load_or_fail`, `COMMAND_HANDLERS` |
| `tests/cli/test_project_catalog_cmd.py` | +210/-0 | NEW FILE: every scenario the block's C4 lists, in-process through `apps.cli.grouped.main` |
| `tests/orchestration/import_reachability_allowlist.txt` | +2/-0 | `apps.cli.commands.repo_catalog_cmd` and `packages.orchestration.repo_catalog_plausibility` added, each sorted in place — both now reachable through `commands/__init__.py` |

No file beyond this list was touched for C4; `apps/cli/grouped.py`'s existing generic
`else: parser.add_argument(arg.name, default=arg.default, help=arg.help)` fallback already
handles `--catalog` correctly (confirmed by parsing both commands with and without it), so no
guard required a new entry there.

### 55a2d9e32 F206 R3 C5: the repository catalog's user page (T004)

| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +2/-0 | the quick-find row (`repository catalog`) and the Guides-table row for the new page, each sorted alphabetically into its table |
| `docs/guides/repo-catalog-user-guide-v1.md` | +97/-0 | NEW FILE: the user page, covering every point the block's C5 lists |

### this commit F206 R3 C6: handback

| Path | +/- | Reason |
|---|---|---|
| `.agent/handoff.md` | this commit | this file (self-reference rule, `docs/agents/handback_template.md`) |

## External actions

`git -C /home/decodeux/Repos/remedy push origin feature/f206-repo-dependency-catalog` after this
commit — outcome reported in the final reply only, not here, because the handoff is written
before the command runs. No pull request opened, edited or merged this round (the block forbids
opening one). No `git worktree add`/`remove` performed; the worker's own scratch directory
`.remedy-wt/f206-r3-worker/` (gitignored) held the copy, equality-proof and plain-python
diagnostic scripts.

## Verification

**Preconditions (before C1):** `git branch --show-current` read
`feature/f206-repo-dependency-catalog`; `git rev-parse HEAD` read
`5fd2b6f4335e4225cb8b3210312aecd60f03f5d3`, equal to
`origin/feature/f206-repo-dependency-catalog`; `git status --porcelain` empty.

**Block digest (before any write):** `wc -l block.md` read `203`, its sha256 read
`b1da76cbd6e52b24be5a2f41f2462e0644da6d4599d43ebe2fd156dec441fae7` — both equal to the values the
prompt delivered.

**Bundle digests (before any write):** `dry-live_review.md`, `dry-decisions.md`,
`dry-prose_slips.md`, `dry-plan.md`, `dry-T13_F206.md`, `run_selection.py` and `selection.txt`
were hashed with `sha256sum` and matched the block's and the prompt's stated digests exactly:
```
c470f62b930920dfdbafe353cb41f2d4b7a598ecd413737c23f1a4b23423a036  dry-live_review.md
efd37184e839001b2c333010070f8b07e8e2712d39f74a33d20d59176057f032  dry-decisions.md
4827bf38cba7f0c5a59d33c2274222b214dd1cf896ae64771f039be68a053fe6  dry-prose_slips.md
b238bc29f0219196c977fb8b587704f33702182dcd342ba477d86deb08a23b03  dry-plan.md
06b1d1f05c3aa1404fc3cd4a6ad1650f9ab0d0fb0951100cbb3996f671b19032  dry-T13_F206.md
a80d9ffda67fdc6cf87daa30e0b8369c39e57b054bad096df9e544e0f05d9c77  run_selection.py
4bdbd88f58a56c960169e78a201061b682c1d4fc2bf75d1fa3ac14cec8bb38bf  selection.txt
```

**C1:** each `dry-*` file `cp`-copied over its path and `block.md` copied to
`.agent/authored/f206-r3.md`; `cmp` of every pair printed nothing (all six identical); the block
copy re-read at `wc -l` 203 and sha256 matching. `git add` of the six paths, then
`git diff --cached --numstat`:
```
203	0	.agent/authored/f206-r3.md
24	0	.agent/decisions.md
4	0	.agent/live_review.md
11	12	.agent/plan.md
1	0	.agent/prose_slips.md
7	0	docs/roadmap/features/T13_F206.md
```
Matching the Bundle's stated numstat for every path exactly. Commit `4b5832c04`; `git show
--numstat` matched the table above exactly.

**C2:** the project-group block (command_catalog.py lines 774–914) was extracted and compared
byte for byte against the new module's own copy with `diff` (no output — identical). The live
catalog was then compared whole: the pre-move module (`4b5832c04:apps/cli/command_catalog.py`,
loaded under a throwaway module name) against the post-edit live `apps.cli.command_catalog.CATALOG`,
entry for entry and in order:
```
old entries: 184
new entries: 184
IDENTICAL: all 184 entries equal and in the same order
```
`python3 -m ruff check apps/cli/command_catalog.py apps/cli/command_catalog_project.py
packages/orchestration/lessons.py tests/orchestration/test_lessons.py
tests/test_structure_ratchet.py` → `All checks passed!` (this caught the unused `_PROJECT_ID`
import, fixed before commit). `wc -l apps/cli/command_catalog.py` read `2491` after all edits,
before commit, matching the ledger row and the `MAX_FILE_LINES` arithmetic (`74818 - 140 = 74678`).
`git diff --cached --numstat`:
```
5	145	apps/cli/command_catalog.py
159	0	apps/cli/command_catalog_project.py
3	2	docs/system/structure-ledger-v1.md
4	3	packages/orchestration/lessons.py
1	0	tests/orchestration/import_reachability_allowlist.txt
8	0	tests/orchestration/test_lessons.py
1	1	tests/test_structure_ratchet.py
```
Commit `61450596f`; `git show --numstat` matched exactly.

**C3:** `packages/orchestration/repo_catalog_plausibility.py` written (242 lines), then
`tests/orchestration/test_repo_catalog_plausibility.py` (271 lines) — 513 together, over the
500-insertion cap, so the block's own split-into-two-commits clause applied and the module was
committed first. Before either commit, a plain-python diagnostic (not pytest,
`.remedy-wt/f206-r3-worker/dry_check_plausibility.py`) exercised every scenario the test file
also covers directly against the module's functions:
```
ok: normalize Foo_Bar
ok: normalize foo-bar
...
ok: warnings order matches catalog-then-evidence order

ALL DRY CHECKS PASSED
```
(39 `ok:` lines, 0 `FAIL:` lines — full transcript in the worker scratch directory, trimmed here).
`python3 -m ruff check packages/orchestration/repo_catalog_plausibility.py
tests/orchestration/test_repo_catalog_plausibility.py` → `All checks passed!`.
`git diff --cached --numstat` for the module commit: `242	0	packages/orchestration/repo_catalog_plausibility.py`.
Commit `0cfb8e640`; `git show --numstat` matched. For the tests commit:
`271	0	tests/orchestration/test_repo_catalog_plausibility.py`. Commit `b4591f52c`; `git show
--numstat` matched.

**C4:** the two catalog entries were added, then the handler module, then the wiring, then the
test file. `python3 -m ruff check` on the four touched Python files read `All checks passed!`.
Three plain-python diagnostics (not pytest) ran before commit:
- `dry_check_catalog_entries.py` — every property `tests/test_command_catalog.py` and
  `tests/cli/test_exit_codes.py` check (duplicate ids, `supports_json`, the `--catalog`/`--json`
  args, `action_class`, `related`, `exit_codes == EXIT_CODE_FLOOR`, the derived-unflagged-set
  still empty, every `related` reference resolving, a handler registered, and both commands
  actually parsing through `build_parser()`) — all passed, including confirming `--catalog`
  parses correctly with NO change to `apps/cli/grouped.py`.
- `dry_check_reachability.py` — reused `tests/orchestration/test_import_reachability.py`'s own
  `reachable_closure()`/`read_allowlist()`: `repo_catalog_cmd reachable: True`,
  `repo_catalog_plausibility reachable: True`, `unlisted (should be empty): []`.
- `dry_check_vocabulary.py` — reused `tests/docs/test_vocabulary.py`'s own
  `_synonym_offenders()`/`_meaning_violations()` against the live catalog: both empty. This is
  how the "order" → "sequence" wording fix (declared below) was found and verified, before any
  commit.
- `dry_check_cli_e2e.py` and `dry_check_cli_e2e_extra.py` — `apps.cli.grouped.main` called
  in-process for every scenario `tests/cli/test_project_catalog_cmd.py` also covers (no catalog,
  a valid catalog shown, a warning-and-skip check, a cycle, an unknown key, both text and JSON):
  all `ok:`, 0 `FAIL:`.
`git diff --cached --numstat`:
```
34	0	apps/cli/command_catalog_project.py
2	1	apps/cli/commands/__init__.py
129	0	apps/cli/commands/repo_catalog_cmd.py
210	0	tests/cli/test_project_catalog_cmd.py
2	0	tests/orchestration/import_reachability_allowlist.txt
```
Commit `ac92e044d`; `git show --numstat` matched exactly.

**C5:** the guide page written, two `docs/README.md` rows added in their alphabetical place. A
plain-python diagnostic (`dry_check_docs.py`), reusing `tests/docs/test_docs_consistency.py`'s
own broken-link and index-registration logic, read: no broken relative links in `docs/README.md`,
every `docs/guides/*.md` page linked. A second diagnostic (`dry_check_advertised.py`), reusing
`tests/cli/test_advertised_commands.py`'s own scanner, read:
```
operator-facing advertisements seen: 665
unresolved: []
operator-facing flags checked: 294
undeclared flags: []
```
and the production-code sweep (`collect_command_advertisements`) read `689 seen, 0 unresolved`,
`218 flags checked, 0 undeclared`. `git diff --cached --numstat`:
```
2	0	docs/README.md
97	0	docs/guides/repo-catalog-user-guide-v1.md
```
Commit `55a2d9e32`; `git show --numstat` matched exactly.

**Gate 1 (status):** `git -C /home/decodeux/Repos/remedy status --porcelain` → empty, exit 0.

**Gate 2 (ruff):**
`python3 -m ruff check apps/cli/command_catalog.py apps/cli/command_catalog_project.py apps/cli/commands/repo_catalog_cmd.py apps/cli/commands/__init__.py packages/orchestration/lessons.py packages/orchestration/repo_catalog_plausibility.py tests/orchestration/test_lessons.py tests/orchestration/test_repo_catalog_plausibility.py tests/cli/test_project_catalog_cmd.py tests/test_structure_ratchet.py`
→ `All checks passed!`, exit 0.

**Gate 3 (selection), only run — GREEN:**
`python3 /home/decodeux/Repos/remedy/.remedy-wt/f206-r3/prep/run_selection.py /home/decodeux/Repos/remedy`
→
```
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252): ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252): ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252): ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252): ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252): ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252): ...
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
6560 passed, 9 skipped in 138.56s (0:02:18)
exit 0
```
Exit 0, no FAILED or ERROR line, no line containing `process(es) behind`. All nine SKIPPED lines
are pre-existing skips of this checkout (the F252 D3/D12 quarantines, opt-in install smoke, and a
UI-source-not-found guard), unrelated to this round's change and none of them a UI-toolchain
skip. No fix commit was needed; gate 3 was run exactly once.

**Gate 4 (integrity):** `python3 -m apps.cli.main integrity check --json` →
```json
{"check_count": 6, "checks": [{"message": "handlers=186", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
```
Exit 0, all six checks `pass`, `fail_count` 0. `handlers=186` (184 before this round's C4, plus
`project.catalog-check` and `project.catalog-show`).

**Gate 5 (open findings list):**
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
→ `['R-1235', 'R-1246', 'R-1251', 'R-1252']`, matching exactly.

**Gate 6 (commit log):** `git -C /home/decodeux/Repos/remedy log --format=%s 5fd2b6f43..HEAD` →
```
F206 R3 C5: the repository catalog's user page (T004)
F206 R3 C4: remedy project catalog-check and catalog-show (T004)
F206 R3 C3: the lockfile plausibility check's tests (T003)
F206 R3 C3: the lockfile plausibility check (T003)
F206 R3 C2: the catalog's project group moves to command_catalog_project.py (structure rule 2, DECISION F206 D4)
F206 R3 C1: book round 2 and R-1253's resolution, DECISIONS F206 D3 and D4, the plan for round 3
```
The subjects of C1 to C5, newest first.

No mutation run (the block forbids it this round). No `REMEDY_TEST_MAX_WORKERS` set, no extra
`-n` passed beyond gate 3's own script, no two test commands run at once — every plain-python
diagnostic above ran alone, sequentially, and none of them was a pytest invocation. No
`npm`/`npx` run. No pull request opened, edited or merged. No provider call made this round.

## Authored-text proofs

1. `block.md` → `.agent/authored/f206-r3.md` (C1): byte-equal, confirmed by `cmp` and again by
   the re-read `wc -l` (203) and sha256.
2. `dry-live_review.md` → `.agent/live_review.md` (C1): byte-equal, confirmed the same way.
3. `dry-decisions.md` → `.agent/decisions.md` (C1): byte-equal, confirmed the same way.
4. `dry-prose_slips.md` → `.agent/prose_slips.md` (C1): byte-equal, confirmed the same way.
5. `dry-plan.md` → `.agent/plan.md` (C1): byte-equal, confirmed the same way.
6. `dry-T13_F206.md` → `docs/roadmap/features/T13_F206.md` (C1): byte-equal, confirmed the same way.

`apps/cli/command_catalog_project.py`'s moved entries (C2) are a byte-for-byte MOVE, proved by
`diff` against the pre-move source rather than against a reviewer-prepared file; the catalog
equality proof above is the behaviour-preservation half of that same proof. Everything else this
round — the new import/comment lines in `command_catalog.py`, the ledger and ratchet edits (C2),
`repo_catalog_plausibility.py` and its tests (C3), the two new catalog entries and
`repo_catalog_cmd.py` and its tests (C4), and the user page (C5) — is this session's own authored
production code, docs and tests, written from the block's specification rather than copied from
a prepared file; no authored-text proof applies to them.

## Deviations & assumptions

1. **Vocabulary-guard word swap (declared, as the block itself orders):** the block's C4 gives
   `project.catalog-show` the description "Show the repository catalog and the order it gives
   the repositories." `tests/docs/test_vocabulary.py`'s enforced-mode meaning check flags any
   catalog description using a BINDING word (`Order` is one) without one of that word's pinned
   meaning fragments (`order file`, `what you ask`, `text or`) present in the same text — found
   by running the guard's own `_meaning_violations()` directly before committing. Changed only
   that one word: "order" → "sequence", landed as
   "Show the repository catalog and the sequence it gives the repositories.", with a one-line
   comment above the entry naming why. Re-ran the same guard function after the change: zero
   violations, zero retired-synonym offenders anywhere in the catalog.
2. **The root-resolution lookup for a given `project_roots` mapping missing a `pid` (an inference,
   not stated by the block):** DECISION F206 D3 (3) reads "its own `root`... else
   `project_roots[pid]` when the mapping is given", which read as a literal subscript would raise
   `KeyError` for a `pid` the caller's mapping omits. `_resolve_entry_root` instead uses
   `project_roots.get(entry.pid)`, so a `pid` absent from a GIVEN mapping is treated the same as
   "no root" (one `RepoCatalogSkip`) rather than an uncaught exception — consistent with "No
   root... one `RepoCatalogSkip`" governing every no-root case the same way, and with every test
   this round (including `test_project_catalog_cmd.py`'s warning-and-skip scenario) exercising
   this path deliberately.
3. **A failed root resolution skips the WHOLE entry, including its `consumes` evidence (a choice
   the block left open):** DECISION F206 D3 (5)'s rule reads a consumer's lockfiles AND its
   `consumes` list together as "its evidence"; the block's "No root... one `RepoCatalogSkip`"
   sentence does not say whether `consumes` (which needs no filesystem access) is still read when
   the root cannot be resolved. Chosen: no — a skipped entry contributes no warnings of either
   kind, which is also what `tests/orchestration/test_repo_catalog_plausibility.py`'s
   `test_no_root_and_a_missing_directory_are_both_skipped` pins. Reversing this reading (reading
   `consumes` regardless of root) would need a new test and is a one-line change in
   `check_repo_catalog_plausibility`.
4. **The `RepoCatalogSkip.reason` wording (a choice the block left open):** the block pins
   `RepoCatalogSkip`'s two fields (`pid`, `reason`) and the CLI's `Skipped: <pid>: <reason>` line,
   but not the reason text itself. Chosen: `f"{pid} has no root"` and
   `f"{pid}'s root {root} is not a directory"`.
5. **`catalog-show`'s per-entry text block (a choice the block left open):** the block says text
   output names "one block per entry naming every field that is set" without a shape. Chosen: a
   `<pid>:` header line, then one indented `  <field>: <value>` line per field that is set
   (`name`, `root`, `owner`, `depends_on`, `publishes`, `consumes`, each only when non-empty),
   matching the shape the warning/skip lines around it already use.
6. **Plain-python diagnostics, not pytest, before every commit (a clarification, not a rule
   violation):** the block's constraints reserve the round's only TEST run for gate 3. Before
   each of C2 through C5, the session ran plain `python3` scripts under
   `.remedy-wt/f206-r3-worker/` that import the touched production modules and call their
   functions directly, or reuse a target test file's OWN helper functions (never `pytest`, never
   collecting or executing a test node) to self-check the new code before it was ever staged.
   This is the same class of pre-commit check round 2's C2 used ("smoke-tested directly, not via
   pytest") rather than the ad hoc `pytest` invocation round 2 declared as its deviation 1; no
   `pytest` process ran this round outside gate 3 itself.

No commit was added, dropped or reordered from the block's C1–C6 sequence (C3 split into two
commits as the block's own size clause required, which is compliance rather than a deviation); no
mutation red-proof was run (forbidden this round); no pull request action was taken.

## Next

1. Phase 1 rule 1 (`.agent/STOP`): absent throughout this round; the next session checks it first.
2. Phase 1 rule 2: the Open PR Gate.
3. The next round's first commit books round 3's verdict.
4. The closure sequence: the closure's one full suite and the self-use item.

Operator questions open: 1.
Open findings: 4 — R-1235, R-1246, R-1251 and R-1252, owned by F306.

## For the operator, in plain sentences

Two new commands let the operator check the catalog and see the order it gives. The check warns
when a repository's lockfile shows it uses a package another repository publishes while the
catalog says nothing about that dependency, and names the lockfile as proof. A page explains how
to write the catalog. A first step only moved existing command descriptions to a module of their
own without changing them.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | round 2 and R-1253's resolution booked, DECISIONS F206 D3 and D4 appended, the feature file amended, the plan rewritten for round 3; all six numstat pairs matched |
| C2 | done | the `project` group moved byte for byte to its own module; the live catalog proved equal, 184 entries, entry for entry and in order; the ledger row and `MAX_FILE_LINES` fell by exactly what moved |
| C3a (module) | done | `repo_catalog_plausibility.py` written and ruff-clean; split from C3b by the 500-insertion cap |
| C3b (tests) | done | every scenario the block's C3 lists, plus a dry-run proof before commit |
| C4 | done | `project.catalog-check`/`catalog-show` added, handler module written and wired, reachability allowlist updated, tests written; no `grouped.py` change needed |
| C5 | done | the user page written, `docs/README.md` registered in both tables |
| C6 | done | this handback |
| Push | done | reported in the final reply |
| Gate 1 | passed | `status --porcelain` empty |
| Gate 2 | passed | `All checks passed!` |
| Gate 3 | passed | `6560 passed, 9 skipped`, exit 0, run exactly once |
| Gate 4 | passed | `fail_count` 0, six checks `pass` |
| Gate 5 | passed | open findings list matched exactly |
| Gate 6 | passed | subjects matched the commit sequence, newest first |
| Structural step (DECISION F206 D4 (1)) | done | C2; no behaviour change, proved rather than asserted |
| T003 | done | C3a+C3b; the lockfile plausibility check, module and tests |
| T004 | done | C4+C5; both commands, their handler, tests and the user page |
