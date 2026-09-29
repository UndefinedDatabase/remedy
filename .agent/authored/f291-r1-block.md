STEP F291 R1 — CLAIM F291 AND LAND T001 AND T002: the self-use generator's Tier 4, the excused blind handlers, and its Tier 5, the test-less modules

GOAL
Pull request 298 is merged; `main` is at `aa5defdee` and F291 Self-use sources v2 is the first
unchecked STATUS line. Cut F291's branch, claim it, re-head the live review record, book F042's
round 11 and record DECISION F291 D1. Then land T001 and T002 against the reviewer's tests: two new
tiers at the end of `packages/orchestration/self_use_generator.py`.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test diff travels as a payload and is the acceptance, and you write the production code
against it and against S1 to S6 below. You never edit a payload; if one looks wrong to you, STOP
and report it. Read DECISION F291 D1 in the claim diff before you write code, and read whole,
before you edit or call them: `packages/orchestration/self_use_generator.py`,
`packages/orchestration/self_use_queue.py` and `tests/test_ble001_ratchet.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f291-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f291-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f291-r1-dry/`, `.remedy-wt/f291-r1-sim/`, `.remedy-wt/f291-scratch/`
                                  The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f291-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd`
your shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace is refused: write such a script to a file
under your own directory and run the file. Set environment variables for a child process inside
a Python script (`subprocess.run(..., env=...)`), never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `aa5defdee`. Report all three. Then
   `git checkout -b feature/f291-self-use-sources-v2` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f291-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f291-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 141 | 15950 | 4254240e907810a39812a5ce7c23ca409dace2bbb38847a61ff43b83714ab534 |
| tests.diff | 399 | 20211 | 9d4c792845887b8474f130edf123052fb81aed9e8fc7363e62fcc04d6659442e |
| plan.md | 29 | 1015 | 0ca34f58fe6701fc6fb04f3410d7fca7dda7903532c92c5c96faa5e4f155cd67 |
| context.md | 35 | 1493 | 6118b07bcc1e4b3b4af08c30919182321514bfe4a5fd6cb3c0c1ad44e2fdd5f0 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. Every
`.diff` goes on with `git apply`; the reviewer generated them with `git diff HEAD` from a tree at
`aa5defdee`. `claim.diff` edits `.agent/live_review.md` (the re-head, which replaces everything
above the `## Findings` heading line, then F042's round 11 gate entry appended),
`.agent/decisions.md` (DECISION F291 D1 appended) and `docs/roadmap/STATUS.md` (F291's line `[ ]`
to `[~]`). `tests.diff` edits `tests/orchestration/test_self_use_generator.py`: one line added to
its autouse fixture and its docstring, and the new test classes appended.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. Every
change is in `packages/orchestration/self_use_generator.py`; no other production file changes.
S0 THE MARK IS NEVER SPELLED. `tests/test_ble001_ratchet.py` counts every line under `packages/`
   that matches `#\s*noqa:\s*BLE001\b`, docstrings and string literals included, so no line you
   write in this module may contain `#` followed by `noqa: BLE001`. Say "BLE001 excuse mark" in
   prose, and compose the job text from `EXCUSE_MARK_WORDS` as S4 states. Add no `except
   Exception` and no mark anywhere.
S1 Module-level names, placed with the other provenance constants:
   `_EXCUSED_PROVENANCE = "generated (self-use-generator tier 4, excused handler, {key})"` with
   `_EXCUSED_PROVENANCE_RE` reading `(?P<key>.+)` back; `_UNTESTED_PROVENANCE =
   "generated (self-use-generator tier 5, untested module, {path})"` with `_UNTESTED_PROVENANCE_RE`
   reading `(?P<path>.+)` back; `EXCUSED_HANDLER_ROOTS = ("packages", "apps", "scripts")`;
   `EXCUSED_HANDLER_MARK = re.compile(r"#\s*noqa:\s*BLE001\b(?P<rest>.*)")`, the ratchet's own
   pattern; `EXCUSE_MARK_WORDS = "noqa: BLE001"`; `RATCHET_TEST_PATH =
   "tests/test_ble001_ratchet.py"`; `UNTESTED_MODULE_ROOTS = ("packages", "apps/cli")`;
   `TESTS_ROOT = "tests"`. A public function `default_source_root() -> Path` returning
   `Path(__file__).resolve().parents[2]`, beside `default_docs_root`.
S2 `generate_self_use_item` and `generate_and_append_if_empty` gain the keyword-only parameter
   `source_root: Path | None = None`, the second passing it to the first. After Tier 3 answers
   None, `root = source_root or default_source_root()`, then Tier 4, then Tier 5, each returning
   its entry when it has one; with neither, the function returns None.
S3 TIER 4's marks: for each root of `EXCUSED_HANDLER_ROOTS` that is a directory under `root`,
   every `*.py` file below it (`rglob`), each line matching `EXCUSED_HANDLER_MARK`, as
   `(relative posix path, line number, the stripped line, key)`, the key being
   `f"{path}:{ordinal}:{text}"` where the ordinal is 1 plus the number of earlier lines of the
   same file with the same stripped text; all marks sorted by path, then line. A file that cannot
   be read as UTF-8 raises `SelfUseGenerationError` naming it, catching `OSError` and
   `UnicodeDecodeError` only. Tier 4 offers the first mark whose key no queue entry's provenance
   targets (consumed or not, read with `_EXCUSED_PROVENANCE_RE`) and whose line
   `RETIRED_WORD` does not match (R-1015).
S4 TIER 4's entry: `id` from `_next_queue_id`, `consumed_by` empty, `why` the stripped line,
   `provenance` `_EXCUSED_PROVENANCE` with the key, `title` `f"Narrow the excused handler at
   {path}:{number}"`, and `job_markdown` exactly these lines, where `{mark}` is
   `f"# {EXCUSE_MARK_WORDS}"`, `{ratchet}` is `RATCHET_TEST_PATH`, and every line ends in `\n`:
     # Job: {title}
     (empty)
     ## Task 1
     Line {number} of `{path}` excuses a blind exception handler from ruff's BLE001 rule:
     (empty)
         {text}                                    <- four spaces, then the stripped line
     (empty)
     Narrow this handler to the exception types the code it guards can really raise, and delete its `{mark}` mark. In the same change lower `MAX_EXCUSED` in `{ratchet}` by one, because that test holds the number of marks equal to it. Add no mark anywhere else, and do not edit any file under `.agent/`.
     (empty)
     Acceptance:
     - The handler at line {number} of `{path}` no longer carries a `{mark}` mark, and `python3 -m ruff check {path}` reports nothing.
     - `python3 -m pytest -q {ratchet}` passes, with `MAX_EXCUSED` one lower than before.
     - No file under `.agent/` is changed by this task.
S5 TIER 5: the names bound by the tests are every `ast.Import` alias name and, for every
   `ast.ImportFrom` with a module and level 0, the module and `f"{module}.{alias}"` for each
   alias, over every `*.py` file below `root / TESTS_ROOT` (none when that is not a directory); a
   test file that does not parse raises `SelfUseGenerationError` naming it. For each root of
   `UNTESTED_MODULE_ROOTS` that is a directory, in that order, every `*.py` below it sorted, skip
   `__init__.py`, a path a queue entry targets (read with `_UNTESTED_PROVENANCE_RE`), a path
   `RETIRED_WORD` matches, and a module whose dotted name (its relative path's parts without the
   suffix, joined by dots) the tests bind. The names to test are the module's top-level
   `FunctionDef`, `AsyncFunctionDef` and `ClassDef` names in source order that do not start with
   `_`, or all of them when none is public; a module with none is skipped. The first module left
   is the entry: `title` `f"Write the first tests for {path}"`, `why` ``f"No file under `tests/`
   imports `{dotted}`."``, `provenance` `_UNTESTED_PROVENANCE` with the path, `consumed_by` empty,
   and `job_markdown` exactly these lines, `{names}` being each name in backticks joined by
   `", "`, and `{stem}` the file's stem:
     # Job: {title}
     (empty)
     ## Task 1
     No file under `tests/` imports `{dotted}`, so nothing tests `{path}` directly. The names to test are {names}.
     (empty)
     Write its first tests, in a test file named after the module, `test_{stem}.py`, beside the tests of its package — a new file, or the existing file of that name if there is one. The file imports `{dotted}` and holds at least one meaningful test for each name above. Change no production code, and do not edit any file under `.agent/`.
     (empty)
     Acceptance:
     - A test file under `tests/` imports `{dotted}`, and pytest passes on it.
     - Each of {names} is exercised by at least one of the new tests.
     - No file under `.agent/` is changed by this task.
S6 THE MODULE DOCSTRING lists Tier 4 and Tier 5 after Tier 3 in the style of the others, naming
   `docs/roadmap/features/T5_F291.md` T001 and T002 and DECISION F291 D1, says the two come last
   because they almost always have an item, adds `default_source_root() -> Path` to the Public
   API list, and adds to "Deliberate absences" that Remedy deliberately does not ask git how old
   a mark is: Tier 4's "oldest" is the first mark in file order. Each new function has a
   one-line docstring naming what it returns.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f291-r1-block.md` := this block, and `.agent/authored/f291-r1-plan.md` and
  `.agent/authored/f291-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F291 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 64. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f291-r1-claim.diff` := claim.diff.
  Subject: `F291 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 141.

C1c — copy the tests diff
  `.agent/authored/f291-r1-tests.diff` := tests.diff.
  Subject: `F291 R1 C1c: copy round 1 tests diff into .agent/authored/`
  Expected insertions: 399.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F291 R1 C2: claim F291, re-head the live review record, book F042 R11, record D1`
  Expected by `git show --numstat` (insertions and deletions): 13/12 .agent/context.md, 60/0 .agent/decisions.md, 20/24 .agent/live_review.md, 15/12 .agent/plan.md, 1/1 docs/roadmap/STATUS.md.

C3 — THE CODE: S0 to S6 in `packages/orchestration/self_use_generator.py`. If this commit would
  reach 500 insertions, STOP and report rather than split.
  Subject: `F291 R1 C3: offer excused blind handlers and test-less modules as self-use items`
  The reviewer's own version of S0 to S6 read 249/2 packages/orchestration/self_use_generator.py.

C4 — THE TESTS: `git apply` tests.diff.
  Subject: `F291 R1 C4: add the reviewer's tests for the excused-handler and test-less-module tiers`
  Expected: 376/1 tests/orchestration/test_self_use_generator.py.

C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f291-r1-mutations.py`.
  Subject: `F291 R1 C5: add the round 1 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F291 R1 C6: rewrite handoff for round 1`
  Then `git push -u origin feature/f291-self-use-sources-v2`. Do NOT create a pull request: the
  branch opens one at F291's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f291-r1-*` copies and tool, the
   paths claim.diff edits, `tests/orchestration/test_self_use_generator.py`, `.agent/plan.md`,
   `.agent/context.md`, `packages/orchestration/self_use_generator.py`, and `.agent/handoff.md`.
   Report the list you measure with `git diff --name-only aa5defdee` at the branch tip after C6.
   Do NOT touch `tests/test_ble001_ratchet.py`, `scripts/self_use_queue.json`,
   `packages/orchestration/self_use_runner.py`, `packages/orchestration/self_use_queue.py`,
   `docs/system/self-use-track-v1.md`, `docs/roadmap/STATUS_closure_protocol.md`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
   `README.md`.
4. Every test tests.diff carries passes against your code unedited, at C4. A payload test is
   never edited to pass; if your code cannot meet one, STOP and report the test and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F291's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f291-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f291-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1493 | 6118b07bcc1e4b3b4af08c30919182321514bfe4a5fd6cb3c0c1ad44e2fdd5f0 |
 | .agent/decisions.md | C2 | 2506789 | 471743e45b2b63ec20c090f6548c8b804b2cfb6a6a5da7547e52aef692d7b8e3 |
 | .agent/live_review.md | C2 | 134582 | a40922bba9016b86cfb61e9285cf46914904a08ae4109ee6d2c31415c3efe2bf |
 | .agent/plan.md | C2 | 1015 | 0ca34f58fe6701fc6fb04f3410d7fca7dda7903532c92c5c96faa5e4f155cd67 |
 | docs/roadmap/STATUS.md | C2 | 58865 | 82c991bad9e9f57e382491b75568b8eaec3c1a759d88a2962668532176133afd |
 | tests/orchestration/test_self_use_generator.py | C4 | 66817 | 47d81e0af52861b03ab08bbd94ce1b4d52d9e805f6f62a40242571965e06d239 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>`, at
 `aa5defdee` and at C2 (the reviewer read `[]` both times); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F042 R11 — the F042 round 11 entry`; F291's STATUS line at C2 read back in full, which
 must read `- [~] F291 — Self-use sources v2`; and `git diff --name-only <C1c> <C2>`, which must
 name exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/self_use_generator.py
 tests/orchestration/test_self_use_generator.py .agent/authored/f291-r1-mutations.py` at C5, with
 its real exit code. Report `git show --numstat <C3>`, and the count of lines of
 `packages/orchestration/self_use_generator.py` at C3 that match `#\s*noqa:\s*BLE001\b`, which
 must be 0. Then, in the primary checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_runner.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_self_use_findings.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C2, the tests
 of this round and the reviewer's own version of S0 to S6 but no `.agent/authored/f291-r1-*`
 copy, and read `668 passed, 1 skipped` at real exit code 0. Your count may differ from it by
 what the round's copies hold, so report the node count of
 `tests/orchestration/test_self_use_generator.py` by `--collect-only -q` (the reviewer's read 86).
 Report every `SKIPPED` line the `-rs` summary prints; the reviewer's run printed exactly one,
 `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12 quarantine. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f291-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/self_use_generator.py` INSIDE that
 worktree (asserting its FROM text occurs exactly once there), runs
 `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_self_use_generator.py`
 with the worktree as the working directory and the worktree's root first on `PYTHONPATH` (set
 through `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation:
 its label, the exit code and the failed count. It runs an unmutated control first and last,
 reports `restored byte-identical: True` after each restore, and ends with a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 Tier 4's marks are sorted in reverse;
  m2 Tier 4 ignores the keys queue entries target;
  m3 Tier 4's key drops the ordinal (always 1);
  m4 Tier 4's key carries the line number in place of the ordinal;
  m5 `EXCUSED_HANDLER_ROOTS` also holds `"tests"`;
  m6 Tier 5 is tried before Tier 4;
  m7 Tier 4 is tried before Tier 3;
  m8 a `from a.b import c` statement binds `a.b` only;
  m9 a package's `__init__.py` is no longer skipped;
  m10 a module with no public name offers nothing (no fallback to its private names);
  m11 Tier 4 no longer screens with `RETIRED_WORD`;
  m12 the Tier 4 task no longer names `MAX_EXCUSED`;
  m13 Tier 5 ignores the paths queue entries target;
  m14 Tier 5's names leave out classes.
 Run it: `git worktree add --detach .remedy-wt/f291-r1-mut <C5>`, then
 `python3 -B .agent/authored/f291-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f291-r1-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S0 to S6, turned every one red with both controls at exit 0. EVERY mutation must exit
 non-zero; a mutation that stays green is reported as green, never papered over, and you then
 STOP and report it, because the tests are the reviewer's. Then
 `git worktree remove --force .remedy-wt/f291-r1-mut`, `git worktree prune`, and report
 `git worktree list | wc -l`.

G5 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 9`, which must show C6, C5, C4, C3, C2, C1c, C1b, C1a and `aa5defdee` in
 that order; `git worktree list | wc -l`, which must equal your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C5 — report what
you measure), every gate's real output and exit code, the authored-text proofs, the item-status
table AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected
action. Report what you ran, not what you expected to find. Your Session section reads SESSION 1
of feature F291, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then round 2 (the run half of T003 and the documentation of both tiers). State the
open-findings count, 0, and the operator-questions count, 0.
