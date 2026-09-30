STEP F043 R5 — THE END-TO-END RUN OVER THE REAL SHELL AND THE USER GUIDE: a browser test in the suite over a real demo job, and the explanation layer documented

GOAL
Book round 4's PASS with R-1115's resolution, record DECISION F043 D5, and land T003's
end-to-end run — a browser test over a real demo job and the cockpit built into the test's own
folder — with the explanation layer's user guide, both the reviewer's payloads.

ROLE AND AUTHORITY
You are the WORKER. AGENTS.md binds you in full: read every file before you edit it, run the
self-review loop before every commit, keep the tree clean, push, and write the handback. You
never issue a verdict and you never merge. THIS ROUND CHANGES NO PRODUCTION CODE: every change is a
payload you apply, and your own work is the gates and the mutation tool of G4, which proves the new
test catches real defects in the production code. You never edit a payload; if one looks wrong to
you, STOP and report it. Read DECISION F043 D5 in the records diff first, and read whole
`tests/ui_server/test_story_export_file_live.py` and `tests/ui_server/test_brain_demo_recording_live.py`,
whose helpers the new test imports.

THE DIRECTORIES, AND ONLY ONE OF THEM IS YOURS
  `.remedy-wt/f043-r5-payloads/`  READ-ONLY. The reviewer's payloads.
  `.remedy-wt/f043-r5/`           READ-ONLY. The reviewer's block.
  `.remedy-wt/f043-scratch/`      The reviewer's scripts; do not touch them.
  `.remedy-wt/f043-r5-worker/`    YOURS for logs and scripts; create it if absent. All are
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
command line. Never run npm or npx yourself. Never stop a process with `pkill -f`.

COMMIT TRAILER — every commit of this round ends with exactly this line, verbatim:
`Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`

BEFORE ANYTHING ELSE
1. `ls .agent/STOP` — if it exists, write the handoff and stop. Report the reading.
2. Your shell must be in the primary checkout, `/home/decodeux/Repos/remedy`; report `pwd`.
   `git status --porcelain` must be empty, `git branch --show-current` must read
   `feature/f043-explanation-layer`, and `git log --oneline -1` must read `0196da46b`. Report all
   three.
3. Verify this block's own bytes (R-0954): measure the line count and sha256 of
   `.remedy-wt/f043-r5/block.md` and compare both with the two readings your delegation message
   states. Report both measured beside both given, and stop if either differs.
4. Report `git worktree list | wc -l` as found.

PAYLOADS — under `.remedy-wt/f043-r5-payloads/`, lines = newline count. Verify each one's line
count, byte count and sha256 BEFORE using it and report every reading. Never retype a payload;
never edit one.

| file | lines | bytes | sha256 |
|---|---|---|---|
| records.diff | 56 | 9533 | 8332e3da4d52de7976953fb68030d42b5a463244c917f48c0822a2ce5384948b |
| docs.diff | 75 | 5124 | 0475ecf932866e18bbce5a761ba8dce0b0c723c4c58cf3098a12168629954dbb |
| tests.diff | 259 | 12814 | e63f92c37e60833cf42368fcd30a0bd5a198eaf65a8fef91b019fbf25011e017 |
| plan.md | 31 | 1169 | 2b4e575a5ff5214b9328771bb748c4ee294bab69f4384d29b6ffabba474c1e8f |

`plan.md` is a REWRITE of `.agent/plan.md`. The three `.diff` files go on with `git apply`; the
reviewer generated them with `git diff HEAD` from a tree at `0196da46b`. `records.diff` appends
round 4's gate entry and R-1115's resolution to `.agent/live_review.md` and DECISION F043 D5 to
`.agent/decisions.md`. `docs.diff` adds the NEW FILE at
`docs/guides/explanation-layer-user-guide-v1.md` and its two rows in `docs/README.md`.
`tests.diff` adds the NEW FILE at `tests/ui_server/test_explanation_layer_live.py`.

BUNDLE — the commits are C1a, C1b, C2, C3, C4, C5 and C6, in this order.

C1a — copy this block and the plan
  `.agent/authored/f043-r5-block.md` := this block and `.agent/authored/f043-r5-plan.md` :=
  plan.md, by `shutil.copyfile`.
  Subject: `F043 R5 C1a: copy round 5 block and plan into .agent/authored/`
  Its insertions are this block's line count plus 31. Report the number you measure.

C1b — copy the three diffs
  `.agent/authored/f043-r5-records.diff`, `.agent/authored/f043-r5-docs.diff` and
  `.agent/authored/f043-r5-tests.diff` := their payloads.
  Subject: `F043 R5 C1b: copy round 5 records, docs and tests diffs into .agent/authored/`
  Expected insertions: 390.

C2 — THE RECORDS: `git apply` records.diff, then rewrite `.agent/plan.md` := plan.md.
  Subject: `F043 R5 C2: book F043 R4 with R-1115's resolution, record D5, advance the plan`
  Expected by `git show --numstat` (insertions and deletions): 36/0 .agent/decisions.md, 4/0 .agent/live_review.md, 11/11 .agent/plan.md.

C3 — THE GUIDE: `git apply` docs.diff.
  Subject: `F043 R5 C3: add the explanation layer's user guide and index it`
  Expected: 2/0 docs/README.md, 49/0 docs/guides/explanation-layer-user-guide-v1.md.

C4 — THE END-TO-END: `git apply` tests.diff.
  Subject: `F043 R5 C4: add the end-to-end run of the explanation layer over the real shell`
  Expected: 253/0 tests/ui_server/test_explanation_layer_live.py.

C5 — THE TOOL: your mutation tool (G4) saved as `.agent/authored/f043-r5-mutations.py`.
  Subject: `F043 R5 C5: add the round 5 mutation tool`

C6 — THE HANDBACK
  `.agent/handoff.md`, rewritten, its own commit, per `docs/agents/handback_template.md`.
  Subject: `F043 R5 C6: rewrite handoff for round 5`
  Then `git push`. Do NOT create a pull request. Report the push's real outcome.

CONSTRAINTS
1. Never edit a payload and never retype one. Run `git apply --check` before each real
   `git apply` and report its exit code.
2. Every commit stays under 500 insertions by the `git show --numstat` reading.
3. The round's whole tracked path set is: the `.agent/authored/f043-r5-*` copies and tool, the
   paths the three diffs edit or add, `.agent/plan.md`, and `.agent/handoff.md`. Report the list
   you measure with `git diff --name-only 0196da46b` at the branch tip after C6. No file under
   `apps/`, `packages/` or `scripts/` changes in this round, and nothing under `docs/roadmap/`.
4. Every test the payloads carry passes unedited at C4. A payload is never edited to pass; if it
   cannot pass, STOP and report it and the reason.
5. If a gate goes red, STOP, commit and push what is verified, write an honest handoff under
   AGENTS.md "If Blocked", and hand back. An EXISTING test that goes red is never edited to pass;
   report it and stop.
6. NOTHING IS MERGED. No `gh pr merge`, no `gh pr create`, no branch switch, no branch deletion,
   no force-push, no `git stash`.
7. Leave every worktree already listed at your step 4, its branch, and every existing stash
   alone. The worktree G4 adds goes under `.remedy-wt/`, is removed as that gate's last action,
   and `git worktree list | wc -l` is reported afterwards.
8. DO NOT run the full suite: amend0917 rule 1 gives a feature exactly one full-suite run and
   F043's belongs to its closure. Run no self-use job and no command that calls a provider; the
   new test runs its demo job on the fake providers.

DONE-WHEN — THE GATES BELOW, every one executed, every reading reported with its real exit
code. "Green" as a word is a finding (guardrail G4). G1 to G4 run before C6 is written.

G1 TRANSPORT — for each payload report the line count, byte count and sha256 you measured
 against the PAYLOADS table. Then compare each `.agent/authored/f043-r5-*` payload copy byte for
 byte with its source (the block copy against `.remedy-wt/f043-r5/block.md`), read back with
 `git show <commit>:<path>` from the commit that added it. Report one reading per copy.

G2 THE RECORDS, THE GUIDE AND THE TEST — the sha256 of each file below, read with
 `git show <commit>:<path>` at the commit named, equals the reviewer's reading, printed from its
 simulation tree. Report each path beside the hash you read:
 | path | at | bytes | sha256 |
 |---|---|---|---|
 | .agent/decisions.md | C2 | 2535317 | 1dd1d1ff968da9e05fc13573ffca9aa13dc3a3a7572cfdc87b396a70517147c2 |
 | .agent/live_review.md | C2 | 130040 | d7f2460573ceb96767b76eecf5ac56a2c7e8ae7b9107d2d92d20f8e863f47ca7 |
 | .agent/plan.md | C2 | 1169 | 2b4e575a5ff5214b9328771bb748c4ee294bab69f4384d29b6ffabba474c1e8f |
 | docs/README.md | C3 | 21228 | df4ad29a0d5a26acf23dac241e5499eeadfafcd9965e64faef557fc6640aa1c0 |
 | docs/guides/explanation-layer-user-guide-v1.md | C3 | 2991 | f74dd530b06dab13a8e7b1076b58df4b854536a87e1f9c35a28ae0f5538120c2 |
 | tests/ui_server/test_explanation_layer_live.py | C4 | 12319 | e842d48458a79c764eb97df84f1eb084128d393599bfd7db006110a0596dc423 |
 Also: the open set by distinct id, computed with `open_finding_ids` from
 `scripts/rotate_live_review.py` over the ledger's TEXT read with `git show <commit>:<path>` at
 `0196da46b` and at C2 (the reviewer read `['R-1115']` and `[]`); the ledger's last non-empty line
 at C2 begins `Done: R-1115 — RESOLVED at`; and `git diff --name-only <C1b> <C2>`, which must name
 exactly the C2 paths of the table above.

G3 THE TESTS — at C5: `python3 -m ruff check .agent/authored/f043-r5-mutations.py
 tests/ui_server/test_explanation_layer_live.py`, with its real exit code. Then, in the primary
 checkout at C5, SERIALLY:
```
bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_explanation_layer_live.py tests/ui_server/test_story_export_file_live.py tests/ui_server/test_brain_demo_recording_live.py tests/ui_contracts tests/orchestration/test_test_runner.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py tests/regression/test_resource_safety.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
```
 The reviewer ran the selection serially in its dry tree, which carries C2, C3 and C4 but no
 `.agent/authored/f043-r5-*` copy and no built `apps/ui/dist`, with the primary's `node_modules`
 linked in, and read `1588 passed, 6 skipped` at real exit code 0, among the skips
 `tests/ui_contracts/test_responsive.py:555` for an unbuilt `dist`, which your checkout has built.
 Report every `SKIPPED` line yours prints, and the outcome of
 `tests/ui_server/test_explanation_layer_live.py::test_the_explanation_layer_works_on_the_real_shell`
 by name. Then `python3 -m apps.cli.main integrity check --json`, which must read all six checks
 `pass` at `fail_count` 0.

G4 THE RED PROOFS — your tool `.agent/authored/f043-r5-mutations.py` takes a worktree path, and
 for each mutation below edits the named production file INSIDE that worktree (asserting its FROM
 text occurs exactly once there), runs `python3 -B -m pytest -q -p no:cacheprovider
 tests/ui_server/test_explanation_layer_live.py` with the worktree as the working directory and
 first on `PYTHONPATH`, restores the bytes, and prints one line per mutation: its label, the exit
 code and the failed count. It runs an unmutated control first and last, reports `restored
 byte-identical: True` after each restore, and ends with `ALL MUTATIONS CAUGHT AND RESTORED
 CLEANLY: <bool>`. Each is a real behaviour change the end-to-end must catch:
  e1 the first-run tour's close no longer records it seen (`apps/ui/src/components/tour/FirstRunTour.tsx`);
  e2 the timeline's Job label carries the key `phase.jobs`, which the catalog lacks
     (`apps/ui/src/components/timeline/PhaseTimeline.tsx`);
  e3 `isHelpShortcut` answers only for "/" (`apps/ui/src/api/termSearch.ts`);
  e4 `firstRunTourDue` answers true only when the key is stored (`apps/ui/src/api/firstRunTour.ts`).
 Run it: `git worktree add --detach .remedy-wt/f043-r5-mut <C5>`, then in Python
 `os.symlink("/home/decodeux/Repos/remedy/apps/ui/node_modules",
 "/home/decodeux/Repos/remedy/.remedy-wt/f043-r5-mut/apps/ui/node_modules",
 target_is_directory=True)`, so the test's own cockpit build resolves the app's imports, then
 `python3 -B .agent/authored/f043-r5-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f043-r5-mut`
 and report its whole output. The reviewer's own version of this probe turned every one red with
 both controls passing. EVERY mutation must exit non-zero; one that stays green is reported as
 green, never papered over, and you then STOP and report it. Then remove the symlink with
 `os.unlink`, `git worktree remove --force .remedy-wt/f043-r5-mut`, `git worktree prune`, and
 report `git worktree list | wc -l`.

G5 TREE AND PUSH — after C6: `git status --porcelain`, which must be empty;
 `git log --oneline -n 8`, which must show C6, C5, C4, C3, C2, C1b, C1a and `0196da46b` in that
 order; `git worktree list | wc -l`, which must equal your step 4 reading; the push's real outcome;
 and `gh pr list --state open --json number,headRefName,baseRefName,isDraft`, which must be EMPTY.
 These readings go in your reply, since C6 cannot contain them.

WHAT TO REPORT
The handback per `docs/agents/handback_template.md`, every section it mandates, INSIDE
`.agent/handoff.md`: the state block, the per-commit changed-files table with the insertion count
you MEASURED beside the one this block expected (report what you measure for C5), every gate's
real output and exit code, the authored-text proofs, the item-status table AGENTS.md requires (one
row per commit and per gate), the deviations, and the next expected action. Report what you ran,
not what you expected to find. Your Session section reads SESSION 1 of feature F043, round 5, and
says in one sentence how much context you had left.

YOUR `## Next` NAMES, IN ORDER: Phase 1 rule 1 (read `.agent/STOP` from disk), the review of
round 5, then the closure sequence's first round (the self-use item, the checklist consolidation
and the feature file's Built State). State the open-findings count, 0, and the operator-questions
count, 0.
