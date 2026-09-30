STEP F044 R1 — CLAIM F044 AND LAND THE PALETTE'S PURE RULES: the fuzzy match, the command list held to the write door, the bar's routing rule held to the chat's parse, and the node jump

GOAL
Pull request 300 is merged; `main` is at `33f66862d` and F044 Command palette, keyboard,
performance budget is the first unchecked STATUS line. Cut F044's branch, claim it, re-head the
live review record, book F043's round 9, record DECISION F044 D1, and land the pure modules
of D1 (1) to (4) against the reviewer's tests.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THE TESTS ARE THE REVIEWER'S AND THE CODE IS YOURS:
the test files and the goldens travel as payloads and are the acceptance, and you write the
production code against them and against S1 to S4 below. You never edit a payload; if one looks
wrong to you, STOP and report it. Read DECISION F044 D1 in the claim diff before you write code,
and read whole, before you write against them: `packages/orchestration/chat_intent.py` (the
routing rule's source), `apps/ui/src/api/termSearch.ts` (a sibling pure module's style),
`apps/ui/src/api/types.ts`'s `RemedyTaskItem` and `RemedyDashboard`, and the `UI_EXPOSED_COMMANDS`
set in `apps/cli/command_catalog.py`.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f044-r1-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f044-r1/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f044-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f044-r1-worker/`    YOURS for logs and scripts; create it if absent. All are
                                  gitignored.

THIS SANDBOX REFUSES SHAPES YOU WILL REACH FOR. Denied: `VAR=x cmd`, `env VAR=x cmd`,
`export VAR=x; cmd`, `cp`, `sed`, process substitution, command substitution, `cd <dir> && git
...`, `for` loops over shell variables, and multi-operation one-liners chained with `;` or `&&`
outside a `bash -c`. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`, and read
`${PIPESTATUS[0]}` when you pipe pytest. Use `git -C <path>` rather than `cd`, and never `cd`
your shell into a worktree. Use `python3 - <<'PY'` for counting, hashing and copying
(`shutil.copyfile`). A heredoc containing a dollar-brace or a brace beside a quote is refused:
write such a script to a file under your own directory and run the file. Set environment
variables for a child process inside a Python script (`subprocess.run(..., env=...)`), never on a
command line. Never run npm or npx yourself: call `apps/ui/node_modules/.bin/tsc`, `.bin/vitest`
and `.bin/eslint` by path. Never stop a process with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read `main`, and
   `git log --oneline -1` must read `33f66862d`. Report all three. Then
   `git checkout -b feature/f044-command-palette` and report the branch. Do NOT pull: the Open PR
   Gate ran before you and `main` is already at the merge commit.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f044-r1/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f044-r1-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| claim.diff | 157 | 17525 | c28e78bdee6acc0c60ec38b12b18b74f68b790e44a072475a04941b1e5cb17f9 |
| tests_ui.diff | 425 | 21143 | 93bb322005a8ddb355ec31140628ec665b30a7dcd052fa6e3bae5dc5c63f0abb |
| tests_py.diff | 193 | 7929 | 18c07f44164255ab745214a074bcd59d1cb2169622d1718bcbf45d6671d760c2 |
| plan.md | 35 | 1329 | 5f1562c04dc3cfe96ced20e470c46c087f295d046d0a0f0384c4f1edac562e94 |
| context.md | 37 | 1568 | 34b0f81709b8c8a8297789451dad718fd7462d06816c17e2b64e5eb2c455e8bd |

`plan.md` and `context.md` are REWRITES of `.agent/plan.md` and `.agent/context.md`. The
`.diff` files go on with `git apply`; the reviewer generated them with `git diff HEAD` from a tree
at `33f66862d`. `claim.diff` edits `.agent/live_review.md` (the re-head, which replaces everything
above the `## Findings` heading line, then F043's round 9 gate entry appended),
`.agent/decisions.md` (DECISION F044 D1 appended) and `docs/roadmap/STATUS.md` (F044's line `[ ]`
to `[~]`). `tests_ui.diff` adds the NEW FILE at `apps/ui/src/api/fuzzyMatch.test.ts`, the NEW FILE
at `apps/ui/src/api/paletteCommands.test.ts`, the NEW FILE at `apps/ui/src/api/paletteJump.test.ts`,
the NEW FILE at `apps/ui/src/api/paletteRouting.goldens.json` and the NEW FILE at
`apps/ui/src/api/paletteRouting.test.ts`. `tests_py.diff` adds the NEW FILE at
`tests/ui_contracts/test_palette_contract.py`, which reads your two TypeScript lists as source
text in a fixed shape (S2 and S3 say which) and runs the goldens through the chat's own parse.

THE SPECIFICATION — the tests are the acceptance; these clauses fix what they leave open. Every
module is pure: no React, no DOM, no storage, no clock, no network, and no new dependency. Each
opens with a header comment naming T5_F044 T001 and DECISION F044 D1.
S1 `apps/ui/src/api/fuzzyMatch.ts`, NEW. Exports the type `FuzzyRange = readonly [number,
   number]` (half-open, in UTF-16 code units over the text as given), the interface `FuzzyMatch`
   (`readonly score: number`, `readonly ranges: readonly FuzzyRange[]`), the interface
   `FuzzyRanked<T>` (`readonly item: T`, `readonly match: FuzzyMatch`), the constants
   `FUZZY_SUBSTRING_BASE = 1000`, `FUZZY_WORD_START_BONUS = 500` and `FUZZY_SUBSEQUENCE_CAP = 499`,
   and two functions. `fuzzyMatch(query, text): FuzzyMatch | null`: FOLDING lower-cases each UTF-16
   code unit ON ITS OWN and keeps a unit whose lower case is longer than one unit as it is, so a
   folded text is exactly as long as the text. The query's runs of white space read as one space
   and its ends are trimmed; an empty result matches with `{ score: 0, ranges: [] }`. A WORD START
   is index 0 or an index whose previous folded unit is not a letter or digit
   (`/[\p{L}\p{N}]/u`). First the CONTIGUOUS hit of the whole folded query: the first occurrence
   that is a word start, else the first occurrence; its score is `FUZZY_SUBSTRING_BASE`, plus
   `FUZZY_WORD_START_BONUS` when it is a word start, minus its index capped at
   `FUZZY_SUBSEQUENCE_CAP`; its one range spans the query. Otherwise the SCATTERED hit: the query's
   units less its spaces, each found at its earliest index after the previous hit, each scoring 1,
   plus 3 at a word start, plus 2 when it directly follows the previous hit; the sum is capped at
   `FUZZY_SUBSEQUENCE_CAP`; the hits merge into maximal ranges; a unit not found answers null.
   `rankFuzzy(items, query, textOf): FuzzyRanked<T>[]` keeps the items whose text matches and
   orders them by score descending, then the shorter text, then the text by plain code-unit
   comparison (`<`, never `localeCompare`), then the order given.
S2 `apps/ui/src/api/paletteCommands.ts`, NEW. Exports the types `PaletteArgKind = "task" |
   "text"` and `PaletteFlow = "send" | "surface" | "form"`, the interfaces `PaletteArg` (`readonly
   name`, `readonly kind: PaletteArgKind`, `readonly required: boolean`, `readonly prompt`) and
   `PaletteCommand` (`readonly command`, `readonly title`, `readonly flow: PaletteFlow`,
   `readonly surface`, `readonly args: readonly PaletteArg[]`), `PALETTE_COMMANDS: readonly
   PaletteCommand[]`, whose entries are EXACTLY those the test "lists every entry exactly as
   DECISION F044 D1's first round wrote it" pins, in that order, `PALETTE_CONTINUATION_COMMANDS:
   readonly string[] = ["job.inject-confirm", "job.inject-answer"];` on one line, and
   `paletteCommandOf(command)`, answering the listed entry or null. THE SHAPE the contract test
   reads, per entry, with no other line inside it: `  {`, then `    command: "<id>",`,
   `    title: "<title>",`, `    flow: "<flow>",`, `    surface: "<surface>",`, then either
   `    args: [],` or `    args: [` with each argument on its own line written exactly as
   `      { name: "<name>", kind: "<kind>", required: <true|false>, prompt: "<prompt>" },` and then
   `    ],`, and last `  },`. The header comment names `UI_EXPOSED_COMMANDS` and
   `apps/cli/command_catalog.py` as the one source, says the continuation steps are left out
   because the add-task sheet owns them, and states the deliberate absence: Remedy deliberately
   does not send a command whose arguments the palette cannot ask for honestly.
S3 `apps/ui/src/api/paletteRouting.ts`, NEW. Exports the type `BarRoute` (`{ readonly kind:
   "none" }`, `{ readonly kind: "chat" }`, `{ readonly kind: "command"; readonly command: string }`
   or `{ readonly kind: "palette" }`), `BAR_QUESTION_WORDS`, `BAR_LEADING_VERBS` and
   `BAR_NOTE_OPENERS` with the values the test "are the chat's words, in the chat's order" pins,
   and `routeBarText(text, focusedTaskId): BarRoute`. THE SHAPE the contract test reads: each list
   declared as `export const <NAME>: readonly string[] = [` and closed by `];`, and the verb table
   declared as `export const BAR_LEADING_VERBS: Readonly<Record<string, string>> = {`, one
   `  <word>: "<command>",` line per verb, closed by a line reading `};`. THE RULE, in this order:
   runs of white space read as one space and the ends are trimmed; a leading "please " (first
   seven units, case ignored) is dropped; an empty line is `none`; a line ending in "?" or opening
   with a question word is `chat`; a first word (case ignored) that is an OWN key of
   `BAR_LEADING_VERBS` is that command; a line opening with a note opener is `job.steer` when
   `focusedTaskId` is not "" and `chat.send` otherwise; a line opening with "run again" is
   `job.rerun-subtree`; anything else is `palette`. A question word, a note opener and "run again"
   count only when no letter, digit or underscore follows them (`(?![\p{L}\p{N}_])`, case ignored,
   the `u` flag). The header comment names `parse_chat_intent` in
   `packages/orchestration/chat_intent.py` as the rule's source and states the tie-break exactly
   as DECISION F044 D1 (3) words it.
S4 `apps/ui/src/api/paletteJump.ts`, NEW. Imports `fuzzyMatch` and its types from `./fuzzyMatch`
   and the dashboard types from `./types`. Exports `JUMP_RESULT_LIMIT = 8`, the interface
   `JumpTarget` (`readonly id`, `readonly nodeId`, `readonly label`, `readonly kind`, strings), the
   type `JumpField = "label" | "id" | "kind"`, the interface `JumpHit` (`readonly target`,
   `readonly field`, `readonly match: FuzzyMatch`), `jumpTargetsOf(dashboard: Pick<RemedyDashboard,
   "tasks">)` (one target per task in order, its `id`, `nodeId`, `label` and `kind`), and
   `rankJumpTargets(targets, query, limit)`: a query that is empty after trimming answers the first
   `limit` targets in their own order, each `{ target, field: "label", match: { score: 0, ranges:
   [] } }`; otherwise each target's match is the highest-scoring of `fuzzyMatch` over its label,
   id and kind, only a STRICTLY higher score replacing the best so far (so the label wins a tie,
   then the id); non-matches drop; rows order by score descending, then the shorter label, then
   the label by code unit, then the order given; and the cut to `limit` comes after that order.

BUNDLE — the commits are C1a, C1b, C1c, C2, C3, C4, C5, C6 and C7, in this order.

C1a — copy this block and the state payloads
  `.agent/authored/f044-r1-block.md` := this block, `.agent/authored/f044-r1-plan.md` := plan.md
  and `.agent/authored/f044-r1-context.md` := context.md, all by `shutil.copyfile`.
  Subject: `F044 R1 C1a: copy round 1 block and state payloads into .agent/authored/`
  Its insertions are this block's line count plus 72. Report the number you measure and
  STOP rather than commit if it is 500 or more.

C1b — copy the claim diff and the contract test diff
  `.agent/authored/f044-r1-claim.diff` := claim.diff and `.agent/authored/f044-r1-tests_py.diff`
  := tests_py.diff.
  Subject: `F044 R1 C1b: copy round 1 claim diff and contract test diff into .agent/authored/`
  Expected insertions: 350.

C1c — copy the vitest diff
  `.agent/authored/f044-r1-tests_ui.diff` := tests_ui.diff.
  Subject: `F044 R1 C1c: copy round 1 vitest diff into .agent/authored/`
  Expected insertions: 425.

C2 — THE CLAIM AND ITS RECORDS, in this order:
   1. `git apply` claim.diff
   2. rewrite `.agent/plan.md` := plan.md
   3. rewrite `.agent/context.md` := context.md
  Subject: `F044 R1 C2: claim F044, re-head the live review record, book F043 R9, record D1`
  Expected by `git show --numstat` (insertions and deletions): 15/14 .agent/context.md, 81/0 .agent/decisions.md, 20/17 .agent/live_review.md, 21/14 .agent/plan.md, 1/1 docs/roadmap/STATUS.md.

C3 — THE CODE: S1 to S4 in one commit. If it would reach 500 insertions, split S1 and S4 into a
  first commit and S2 and S3 into a second, and say so.
  Subject: `F044 R1 C3: add the palette's fuzzy match, command list, routing rule and jump`
  The reviewer's own version of S1 to S4 read 134/0 apps/ui/src/api/fuzzyMatch.ts, 195/0 apps/ui/src/api/paletteCommands.ts, 69/0 apps/ui/src/api/paletteJump.ts, 72/0 apps/ui/src/api/paletteRouting.ts.

C4 — THE VITEST TESTS: `git apply` tests_ui.diff.
  Subject: `F044 R1 C4: add the reviewer's vitest tests and routing goldens for the palette`
  Expected: 108/0 apps/ui/src/api/fuzzyMatch.test.ts, 82/0 apps/ui/src/api/paletteCommands.test.ts, 73/0 apps/ui/src/api/paletteJump.test.ts, 37/0 apps/ui/src/api/paletteRouting.goldens.json, 95/0 apps/ui/src/api/paletteRouting.test.ts.

C5 — THE CONTRACT TEST: `git apply` tests_py.diff.
  Subject: `F044 R1 C5: add the reviewer's contract test holding the palette to Python`
  Expected: 187/0 tests/ui_contracts/test_palette_contract.py.

C6 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f044-r1-mutations.py`.
  Subject: `F044 R1 C6: add the round 1 mutation tool`

C7 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F044 R1 C7: rewrite handoff for round 1`
  Then `git push -u origin feature/f044-command-palette`. Do NOT create a pull request: the branch
  opens one at F044's closure. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading; C3's own clause
   says what to do if it would not.
3. The round's whole tracked path set is: the `.agent/authored/f044-r1-*` copies and tool, the
   paths the diffs edit or add, `.agent/plan.md`, `.agent/context.md`, the files S1 to
   S4 name, and `.agent/handoff.md`. Report the list you measure with `git diff --name-only
   33f66862d` at the branch tip after C7. Do NOT touch `apps/ui/src/components/`,
   `packages/`, `apps/cli/`, `apps/ui/package.json`, `docs/roadmap/features/`, `docs/ui/`,
   `.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or `README.md`.
4. Every test the payloads carry passes against your code unedited, at C5. A payload is never
   edited to pass; if your code cannot meet one, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. Do not repair the reviewer's payloads. An EXISTING test
   that goes red is never edited to pass; report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no checkout of `main` after the
   branch is cut, no branch deletion, no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F044's belongs to its closure. Run no self-use job and no command that calls a provider.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C7 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f044-r1-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f044-r1/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE CLAIM AND THE TESTS — the sha256 of each file below, read with `git show <commit>:<path>`
 at the commit named, equals the reviewer's reading, printed from its simulation tree. Report
 each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/context.md | C2 | 1568 | 34b0f81709b8c8a8297789451dad718fd7462d06816c17e2b64e5eb2c455e8bd |
 | .agent/decisions.md | C2 | 2544175 | b2845a5830d81f78589851a324c86ca172509e535b7604edff59dc5f402b7e0c |
 | .agent/live_review.md | C2 | 125703 | 6d6213310a2a572be189e4102069e2df02a051a07b7fee57f888a9d8df33a5fe |
 | .agent/plan.md | C2 | 1329 | 5f1562c04dc3cfe96ced20e470c46c087f295d046d0a0f0384c4f1edac562e94 |
 | docs/roadmap/STATUS.md | C2 | 59615 | 7347ebc2bc1a34d22621e6309f05958186144250d8a8b01278ed6c4d7b5ac2c2 |
 | apps/ui/src/api/fuzzyMatch.test.ts | C4 | 4486 | 4a30ae79704c6ebd4e765d5972c816180c6303413acd16e4b93078f6ebd1131c |
 | apps/ui/src/api/paletteCommands.test.ts | C4 | 4913 | d26986480ae71ec840a42ebe35b403a9375d46e2762e3e150f66f4265821ffb7 |
 | apps/ui/src/api/paletteJump.test.ts | C4 | 3133 | b85327680d03cdf402fce142f5dda99777e087153bc0d31353f81df70e328a09 |
 | apps/ui/src/api/paletteRouting.goldens.json | C4 | 2903 | ac6bba3999260ff647ee5eebcfa23860036daea7d355dfa14945d28891a5382b |
 | apps/ui/src/api/paletteRouting.test.ts | C4 | 4230 | 0dcfa3b732d9990e04d2eb5cba8dd28b5c1eb512f6f4c196f6abc1d20873dd6c |
 | tests/ui_contracts/test_palette_contract.py | C5 | 7509 | 8dcb55a12a7e9323901483ee1a3354791f7bff4673273f62e1d0472152acc106 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>`, at
 `33f66862d` and at C2 (the reviewer read `[]` both times); at C2 the ledger has exactly one line
 reading `## Findings` and exactly one reading `## Steps`, and its last non-empty line begins
 `Gate: F043 R9 — the F043 round 9 entry`; F044's STATUS line at C2 read back in full, which must
 read `- [~] F044 — Command palette, keyboard, performance budget`; and `git diff --name-only
 <C1c> <C2>`, which must name exactly the C2 paths of the table above.

G3 THE CODE AND THE TESTS — at C6: `python3 -m ruff check .agent/authored/f044-r1-mutations.py
 tests/ui_contracts/test_palette_contract.py`, and `apps/ui/node_modules/.bin/eslint
 --max-warnings 0 src/api/fuzzyMatch.ts src/api/fuzzyMatch.test.ts src/api/paletteCommands.ts
 src/api/paletteCommands.test.ts src/api/paletteJump.ts src/api/paletteJump.test.ts
 src/api/paletteRouting.ts src/api/paletteRouting.test.ts` run with `apps/ui` as its working
 directory, each with its real exit code. Report `git show --numstat <C3>`. Then, in the primary
 checkout at C6, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_chat_intent.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 This selection runs `tsc --noEmit` (`test_typescript_compiles`), the whole vitest suite
 (`test_vitest_passes`) and eslint over `apps/ui/src` (`tests/ui_contracts/test_ui_lint.py`);
 name each of those nodes' outcomes. The reviewer ran the selection serially in its dry tree,
 which carries C2, this round's tests and the reviewer's own version of S1 to S4 but no
 `.agent/authored/f044-r1-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1724 passed, 6 skipped` at real exit code 0, its skips the four D3
 quarantine nodes of `test_graph_architecture.py` and `test_ux_quality.py`, the D12 quarantine and
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout may have
 built; through the primary's binaries in the same tree `tsc` read exit 0 and the whole vitest
 suite `2050 passed | 5 skipped` over 107 files at exit 0. Your counts may differ from those by
 what the round's copies and your `dist` hold: report every `SKIPPED` line yours prints, the
 vitest counts of the new test files (the reviewer's read 17, 7, 7 and 7 for
 `fuzzyMatch`, `paletteCommands`, `paletteJump` and `paletteRouting`), and the pytest count of
 `tests/ui_contracts/test_palette_contract.py` on its own (the reviewer's read `43 passed`).
 Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks `pass`
 at `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f044-r1-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its
 FROM text occurs exactly once there), runs the named checks, restores the bytes, and prints one
 line per mutation: its label, and per check the exit code and the failed count. Vitest runs as
 `<primary>/apps/ui/node_modules/.bin/vitest run --root <worktree>/apps/ui --config
 <primary>/apps/ui/vitest.config.ts src/api/fuzzyMatch.test.ts src/api/paletteCommands.test.ts
 src/api/paletteJump.test.ts src/api/paletteRouting.test.ts` with `<worktree>/apps/ui` as the
 working directory (checklist item 33); the contract test as `python3 -m pytest -q -p
 no:cacheprovider tests/ui_contracts/test_palette_contract.py` with `<worktree>` as the working
 directory. The primary is `/home/decodeux/Repos/remedy`. The tool runs an unmutated control of
 both checks first and last, reports `restored byte-identical: True` after each restore, and ends
 with `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: <bool>`. Each is a real behaviour change, and
 the checks named are those it must turn red:
  f1 the fold lower-cases the whole text at once instead of each code unit on its own
     (`fuzzyMatch.ts`, vitest);
  f2 the contiguous hit takes the first occurrence even when a later one begins a word (same);
  f3 the index subtracted from a contiguous hit is not capped (same);
  f4 the scattered hit's 2 for a unit right after the previous hit is dropped (same);
  f5 `rankFuzzy` drops its shorter-text tie-break (same);
  c1 the `job.preview-stop` entry is removed (`paletteCommands.ts`, vitest and the contract test);
  c2 `job.veto-task`'s title reads "Veto a task" (same, both);
  r1 the verb check runs before the question check (`paletteRouting.ts`, vitest);
  r2 a word no longer needs to be whole: the lookahead after the question words, the note openers
     and "run again" is dropped (same);
  r3 a leading "please " is no longer dropped (same);
  r4 a note routes to `chat.send` even with a focused task (same);
  r5 "should" joins the question words (same, vitest and the contract test);
  j1 a field that only TIES the best so far replaces it (`paletteJump.ts`, vitest);
  j2 a blank query is ranked like any other instead of listing the first targets in order (same);
  j3 the targets are cut at the limit before they are ranked (same).
 Run it: `git worktree add --detach .remedy-wt/f044-r1-mut <C6>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f044-r1-mut/apps/ui/node_modules",
 target_is_directory=True)`, then
 `python3 -B .agent/authored/f044-r1-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f044-r1-mut`
 and report its whole output. The reviewer's own version of this probe, run against its version
 of S1 to S4, turned every one red with every control passing. EVERY mutation must turn every
 check named for it red; one that stays green is reported as green, never papered over, and you
 then STOP and report it. Then remove the symlink with `os.unlink`, `git worktree remove --force
 .remedy-wt/f044-r1-mut`, `git worktree prune`, and report `git worktree list | wc -l`.

G5 TREE AND PUSH — after C7: `git status --porcelain`, which must be empty;
 `git log --oneline -n 10`, which must show C7, C6, C5, C4, C3, C2, C1c, C1b, C1a and
 `33f66862d` in that order (one more line if C3 was split); `git worktree list | wc -l`, which must
 equal your step 4 reading; the push's real outcome; and `gh pr list --state open --json
 number,headRefName,baseRefName,isDraft`, which must be EMPTY. These readings go in your reply,
 since C7 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (none is expected for C3's own files beyond the
reviewer's reading, and none for C6 — report what you measure), every gate's real output and exit
code, the authored-text proofs, the item-status table AGENTS.md requires (one row per commit and
per gate), the deviations, and the next expected action. Report what you ran, not what you
expected to find. Your Session section reads SESSION 1 of feature F044, round 1, and says in one
sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 1, then the bar's dropdown sheet over these four rules. State the open-findings count, 0,
and the operator-questions count, 0.
