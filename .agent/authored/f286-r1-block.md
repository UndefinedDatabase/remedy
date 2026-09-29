STEP F286 R1 — CLAIM F286 AND LAND T001: the staleness catalog's config-key check leaves out a backticked file name (R-1104)

GOAL
Pull request 293 is merged; `main` is at `6ba1f4be` and F286, the fifth findings paydown, is the
first unchecked STATUS line. The open set is R-1104 alone, which F286 owns. Cut F286's branch,
claim it, re-head the live review record, book F039's round 13 verdict, record DECISION F286 D1
and write F286's slice list. Then land T001, R-1104's repair: `_run_c07` in
`packages/orchestration/doc_staleness.py` leaves out a backticked span whose last segment is a file
extension, with the tests that hold `story.html` out of the check while an unregistered
`story.speed` is still reported, and red proofs.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED: you
write the code, its tests and the mutation tool yourself against S1 to S5 below. Only the
`.agent/` records and the two roadmap files travel as payloads. Read DECISION F286 D1 in the claim
diff and R-1104's paragraph in `.agent/live_review.md` before you write code. Before you write
anything, read whole: `packages/orchestration/doc_staleness.py` and
`tests/orchestration/test_doc_staleness.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f286-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f286-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f286-r1-dry/`, `.remedy-wt/f286-r1-sim/`, `.remedy-wt/f286-r1-drafts/`,
  `.remedy-wt/f286-r1-scratch/`   The reviewer's trees and scripts; do not touch them.
  `.remedy-wt/f286-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, and multi-operation one-liners chained with `;` or `&&` outside a `bash -c`. Capture real
exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read `${PIPESTATUS[0]}` when you pipe
pytest. Use `git -C <path>` rather than `cd`, and never `cd` your shell into a worktree. Use
`python3 - <<'PY'` for counting, hashing and copying (`shutil.copyfile`). A heredoc containing a
dollar-brace is refused: write such a script to a file under your own directory and run the
file. Set environment variables for a child process inside a Python script (`subprocess.run(...,
env=...)`), never on a command line. Never run npm or npx.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `6ba1f4be8`. Report all three. Then
   `git checkout -b feature/f286-findings-paydown-v5` and report the branch. Do NOT pull: the
   Open PR Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f286-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f286-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 136 | 14751 | 2eef7c40818affe7e0d704f2d8b54119376eee2c850cb924d086004458d626cf |
| plan.md | 26 | 837 | 69846d69cdf2db528a55e7c525b4122de3740c1c4587544f2bfa987a9c98f6ad |
| context.md | 31 | 1188 | d846742f8054fc14346046c785c6dd4cd8b5e30d314b614237288146c1829797 |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`.
`claim.diff` goes on with `git apply`; the reviewer generated it with `git diff HEAD` from a tree at
`6ba1f4be` into which it wrote the edits. It edits `.agent/live_review.md` (the re-head, which
replaces everything above the `## Findings` heading line, then F039's round 13 gate entry
appended), `.agent/decisions.md` (DECISION F286 D1 appended), `docs/roadmap/STATUS.md` (F286's line
`[ ]` to `[~]`) and `docs/roadmap/features/T2_F286.md` (the Task slicing section, before its
Acceptance heading).

THE SPECIFICATION — the only production file is `packages/orchestration/doc_staleness.py`.
S1 THE SET. Directly under the `# C07 — doc_config_keys` section's closing rule line, a module
   constant `_FILE_EXTENSIONS`, a `frozenset` of exactly these strings: `css`, `html`,
   `js`, `json`, `md`, `py`, `sh`, `toml`, `ts`, `tsx`, `txt`, `yaml`, `yml`. Above it, a comment of
   at most two lines saying that no config key ends in a file extension, so a span whose last
   segment is one is a file name that begins with a key prefix, and naming R-1104.
S2 THE SKIP. In `_run_c07`, after the test that the span's first segment is a key prefix and
   before the command-id test, a span whose LAST dot-separated segment is in `_FILE_EXTENSIONS`
   is skipped. Nothing else in `_run_c07` changes, and no other check changes.
S3 THE CATALOG TEXT. The `doc_config_keys` entry of `CHECKS` has its claim text, the third
   argument, read exactly
   `reads every backticked span that is a whole dotted key name whose first segment is a registered key prefix and whose last is not a file extension`
   on one line; its other arguments are unchanged.
S4 THE FIXTURE TEST, in `TestC07DocConfigKeys` of `tests/orchestration/test_doc_staleness.py`,
   after `test_fresh`: a test writing `docs/guides/story.md` under `tmp_path` whose text backticks
   `story.html` and, in the same paragraph, the unregistered `story.speed`, run with
   `_truth(config_keys=frozenset({"data_dir", "story.step_ms"}))`, asserting with `_fields` that
   the `doc_config_keys` claims are exactly ONE whole literal list of one claim: the check id
   "doc_config_keys", the document "docs/guides/story.md", the claim
   "backticks the config key `story.speed`" and the truth
   "`story.speed` is not a registered config key", each string being the text between the double
   quotes. A one-line comment names R-1104.
S5 THE LIVE GUARD, in `TestAgainstTheRealTree` of the same file: a test asserting that the list
   of `ShippedTruth.live().config_keys` whose last dot-separated segment is in `_FILE_EXTENSIONS`
   is `[]`, with a one-line docstring saying C07 would never check such a key. It imports
   `_FILE_EXTENSIONS` inside its own body.

BUNDLE — the commits are C1a, C1b, C2, C3, C4 and C5, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f286-r1-block.md` := this block, and `.agent/authored/f286-r1-plan.md` and
  `.agent/authored/f286-r1-context.md` := plan.md and context.md. All by `shutil.copyfile`.
  Subject: `F286 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 57. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff
  `.agent/authored/f286-r1-claim.diff` := claim.diff.
  Subject: `F286 R1 C1b: copy round 1 claim diff into .agent/authored/`
  Expected insertions: 136.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F286 R1 C2: claim F286, re-head the live review record, book F039 R13, record D1`
  Expected by `git show --numstat` (insertions and deletions): 9/13 context.md, 37/0 decisions.md, 22/21 live_review.md, 13/13 plan.md, 1/1 STATUS.md, 7/0 T2_F286.md.

C3 — THE REPAIR: S1 to S3 in `packages/orchestration/doc_staleness.py`.
  Subject: `F286 R1 C3: leave a backticked file name out of the config-key check (R-1104)`

C4 — THE TESTS AND THE TOOL: S4 and S5 in `tests/orchestration/test_doc_staleness.py`, and your
  mutation tool (G4) saved as `.agent/authored/f286-r1-mutations.py`.
  Subject: `F286 R1 C4: hold story.html out of the config-key check and add the mutation tool`

C5 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F286 R1 C5: rewrite handoff for round 1`
  Then `git push -u origin feature/f286-findings-paydown-v5`. Do NOT create a pull request: the
  branch opens one at F286's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before the real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f286-r1-*` copies and tool, the
   four paths claim.diff edits, `.agent/plan.md`, `.agent/context.md`,
   `packages/orchestration/doc_staleness.py`, `tests/orchestration/test_doc_staleness.py`, and
   `.agent/handoff.md`. Report the list you measure with `git diff --name-only 6ba1f4be8` at the
   branch tip after C5. Do NOT touch `docs/guides/story-user-guide-v1.md`,
   `scripts/self_use_queue.json`, `.agent/prose_slips.md`, `.agent/candidates.md`,
   `.agent/operator_questions.md` or `README.md`.
4. You write no `Done:` line and no `Landed:` line: the reviewer authors R-1104's resolution at
   the next gate.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. A test this round
   itself wrote that is wrong may be corrected before C5, and the correction is declared. An
   EXISTING test that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F286's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C5 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f286-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f286-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM — the sha256 of each file below, read with `git show <C2>:<path>`, equals the
 reviewer's reading, printed from its simulation tree. Report each path beside the hash you read:
 | path | bytes | sha256 |
 |---|---|---|
 | .agent/context.md | 1188 | d846742f8054fc14346046c785c6dd4cd8b5e30d314b614237288146c1829797 |
 | .agent/decisions.md | 2447895 | 40afe22f0d34900c7a798c98afa2041c2efd3a16c854e032395d7206457b9b2d |
 | .agent/live_review.md | 319065 | 814efda4df948a7575add10a1e258adf3bd699d24e19e064196857c0df277e2d |
 | .agent/plan.md | 837 | 69846d69cdf2db528a55e7c525b4122de3740c1c4587544f2bfa987a9c98f6ad |
 | docs/roadmap/STATUS.md | 57372 | 86fe6b4aa4728e167e702fc004a0303ee69d5e9f3fa52288a26bf6472c010992 |
 | docs/roadmap/features/T2_F286.md | 3248 | 03590ab2b43cc1b843070320560e6cf32a0c7020346ac985bdebc5255f6ab9d3 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the file's TEXT read with `git show <commit>:<path>`, at
 `6ba1f4be8` and at C2 (the reviewer read `['R-1104']` at both); at C2 the ledger has exactly one
 line reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F039 R13 — `; F286's STATUS line at C2 read back in full, which must read
 `- [~] F286 — Findings paydown v5`; and `git diff --name-only <C1b> <C2>`, which must name
 exactly the paths of the table above.

G3 THE CODE AND THE TESTS — `python3 -m ruff check packages/orchestration/doc_staleness.py
 tests/orchestration/test_doc_staleness.py .agent/authored/f286-r1-mutations.py` at C4, with its
 real exit code. Report, quoted from `git show <C3>`, the whole of `_FILE_EXTENSIONS` with its
 comment and the whole of `_run_c07`. Report, from a Python run in the primary checkout at C4,
 `[c for c in run_staleness_checks() if c.check_id == "doc_config_keys"]`, which the reviewer read
 as `[]` with the same repair in its simulation tree, where the same call at `6ba1f4be` answers the
 one claim about `story.html`. Then, in the primary checkout at C4, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_doc_staleness.py tests/orchestration/test_self_use_generator.py tests/orchestration/test_self_use_queue.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_development_artifact_boundary.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -6; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran this selection serially inside its simulation tree, which carries C2 of this
 round and the reviewer's own version of S1 to S5 but no `.agent/authored/f286-r1-*` copy, and
 read `576 passed, 1 skipped` at real exit code 0. Your count may differ from it by what your own tests
 and the round's copies hold, so report the node count of
 `tests/orchestration/test_doc_staleness.py` by `--collect-only -q` (the reviewer's reads 33).
 Report every `SKIPPED` line the `-rs` summary prints; the reviewer's run printed exactly one,
 `SKIPPED [1] tests/test_agent_tooling.py:43`, the D12 quarantine. Then
 `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass` at
 `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f286-r1-mutations.py` takes a worktree path, and
 for each mutation below edits `packages/orchestration/doc_staleness.py` INSIDE that worktree
 (asserting its FROM text occurs exactly once there), runs
 `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_doc_staleness.py` with the
 worktree as the working directory and the worktree's root first on `PYTHONPATH` (set through
 `subprocess.run(..., env=...)`), restores the bytes, and prints one line per mutation: its label,
 the exit code and the failed count. It runs an unmutated control first and last, reports
 `restored byte-identical: True` after each restore, and ends with a final line
 `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change:
  m1 the skip of S2 is deleted;
  m2 `html` is removed from `_FILE_EXTENSIONS`;
  m3 the skip reads the span's FIRST segment instead of its last;
  m4 `host` is added to `_FILE_EXTENSIONS`, which hides the registered key `ollama.host`.
 Run it: `git worktree add --detach .remedy-wt/f286-r1-mut <C4>`, then
 `python3 -B .agent/authored/f286-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f286-r1-mut`
 and report its whole output. EVERY mutation must exit non-zero; a mutation that stays green is
 reported as green, never papered over, and you then add the test that catches it in C4 before C5
 and re-run the tool. Then `git worktree remove --force .remedy-wt/f286-r1-mut`,
 `git worktree prune`, and report `git worktree list | wc -l`.

G5 TREE AND PUSH — after C5: `git status --porcelain`, which must be empty;
 `git log --oneline -n 7`, which must show C5, C4, C3, C2, C1b, C1a and `6ba1f4be8` in that
 order; `git worktree list | wc -l`, which must equal your step 4 reading; the push's real
 outcome; and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which
 must be EMPTY. These readings go in your reply, since C5 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3 and C4 — report what you
measure), every gate's real output and exit code, the authored-text proofs, the item-status table
AGENTS.md requires (one row per commit and per gate), the deviations, and the next expected action.
Report what you ran, not what you expected to find. Your Session section reads SESSION 1 of
feature F286, round 1, and says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then the closure sequence's integration-gate round. State the open-findings count, 1,
and the operator-questions count, 1.
